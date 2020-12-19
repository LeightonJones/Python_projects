def range_sum(numbers, start, end):
    output = 0
    for i in numbers:
        if start <= i <= end:
            output += i

    return output


input_numbers = map(int, input().split())
a, b = map(int, input().split())
print(range_sum(input_numbers, a, b))
