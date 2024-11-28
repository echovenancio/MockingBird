function test_add(fn)
    a = 2; b = 2
    expected = a + b
    result = fn(a, b)
    message = string.format("expected %d, but got %d instead", expected, result)
    assert(result == expected, message)
end

test_add(add_fn)
