use std::fs;
use std::io::read_to_string;

use mlua::{ExternalError, Lua, LuaNativeFn, ObjectLike};
use tonic::{transport::Server, Request, Response, Status};

use sandbox::code_runner_server::{CodeRunner, CodeRunnerServer};
use sandbox::{SolutionReply, SolutionRequest};

use mlua::prelude::*;

pub mod sandbox {
    tonic::include_proto!("sandbox"); // The string specified here must match the proto package name
}

#[derive(Debug, Default)]
pub struct LuaCodeRunner {}

#[tonic::async_trait]
impl CodeRunner for LuaCodeRunner {
    async fn run_user_solution(
        &self,
        request: Request<SolutionRequest>, // Accept request of type HelloRequest
    ) -> Result<Response<SolutionReply>, Status> { // Return an instance of type HelloReply
        let lua = Lua::new();
        let req = request.into_inner();
        let test_case = fs::read_to_string(req.test_path.as_str()).expect("cant find the test case");
        let env = lua.create_table().expect("couldnt create env table");
        let lua_string: LuaTable = lua.globals().get("string").expect("error getting string");
        let lua_assert: LuaFunction = lua.globals().get("assert").expect("error getting assert");
        env.set("string", lua_string).expect("error setting print");
        env.set("assert", lua_assert).expect("error setting print");
        let _ = lua.load(req.solution).set_environment(env.clone()).exec();
        match lua.load(test_case).set_environment(env).exec() {
            Ok(_) => {
                let reply = SolutionReply {
                    code: 0,
                    result: String::from("ok"), // We must use .into_inner() as the fields of gRPC requests and responses are private
                };
                Ok(Response::new(reply)) // Send back our formatted greeting
            },
            Err(err) => {
                let reply = SolutionReply {
                    code: 1,
                    result: err.to_string()
                };
                Ok(Response::new(reply))
            }
        }
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "[::1]:50051".parse()?;
    let greeter = LuaCodeRunner::default();

    Server::builder()
        .add_service(CodeRunnerServer::new(greeter))
        .serve(addr)
        .await?;

    Ok(())
}
