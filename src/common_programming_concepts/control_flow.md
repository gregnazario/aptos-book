# Control Flow

Control flow statements allow you to control the execution path of your Move programs. Move provides several control flow constructs that enable conditional execution, loops, and pattern matching.

## If Statements

If statements allow you to execute different code blocks based on whether a condition is true or false.

### Basic If Statement

```move
module my_module::control_flow {
    public fun basic_if(x: u64): u64 {
        if (x > 10) {
            x * 2
        } else {
            x
        }
    }
}
```

### If-Else Statement

```move
public fun if_else_example(age: u64): String {
    if (age < 18) {
        string::utf8(b"Minor")
    } else if (age < 65) {
        string::utf8(b"Adult")
    } else {
        string::utf8(b"Senior")
    }
}
```

### If Statement with Multiple Conditions

```move
public fun complex_condition(x: u64, y: u64): bool {
    if (x > 0 && y > 0 && x + y < 100) {
        true
    } else {
        false
    }
}
```

### If Statement with Function Calls

```move
public fun validate_input(input: u64): bool {
    if (input == 0) {
        return false
    };
    
    if (input > 1000) {
        return false
    };
    
    true
}
```

## While Loops

While loops execute a block of code repeatedly as long as a condition remains true.

### Basic While Loop

```move
public fun count_down(n: u64): u64 {
    let counter = n;
    while (counter > 0) {
        counter = counter - 1;
    };
    counter
}
```

### While Loop with Break

```move
public fun find_first_positive(numbers: vector<u64>): u64 {
    let i = 0;
    let len = vector::length(&numbers);
    let result = 0u64;
    
    while (i < len) {
        let current = *vector::borrow(&numbers, i);
        if (current > 0) {
            result = current;
            break
        };
        i = i + 1;
    };
    
    result
}
```

### While Loop with Continue

```move
public fun sum_positive_numbers(numbers: vector<u64>): u64 {
    let i = 0;
    let len = vector::length(&numbers);
    let sum = 0u64;
    
    while (i < len) {
        let current = *vector::borrow(&numbers, i);
        i = i + 1;
        
        if (current == 0) {
            continue
        };
        
        sum = sum + current;
    };
    
    sum
}
```

### Infinite While Loop with Break

```move
public fun find_element(numbers: vector<u64>, target: u64): bool {
    let i = 0;
    let len = vector::length(&numbers);
    
    while (true) {
        if (i >= len) {
            break false
        };
        
        let current = *vector::borrow(&numbers, i);
        if (current == target) {
            break true
        };
        
        i = i + 1;
    }
}
```

## For Loops

For loops allow you to iterate over ranges or collections. Move supports for loops with range syntax.

### Basic For Loop with Range

```move
public fun sum_range(start: u64, end: u64): u64 {
    let sum = 0u64;
    for (i in start..end) {
        sum = sum + i;
    };
    sum
}
```

### For Loop with Step

```move
public fun sum_even_numbers(max: u64): u64 {
    let sum = 0u64;
    for (i in 0..max) {
        if (i % 2 == 0) {
            sum = sum + i;
        };
    };
    sum
}
```

### For Loop with Vector Iteration

```move
public fun sum_vector_elements(numbers: vector<u64>): u64 {
    let sum = 0u64;
    let len = vector::length(&numbers);
    
    for (i in 0..len) {
        let element = *vector::borrow(&numbers, i);
        sum = sum + element;
    };
    
    sum
}
```

### For Loop with Early Exit

```move
public fun find_index(numbers: vector<u64>, target: u64): u64 {
    let len = vector::length(&numbers);
    
    for (i in 0..len) {
        let current = *vector::borrow(&numbers, i);
        if (current == target) {
            return i
        };
    };
    
    len // Return length if not found
}
```

### Nested For Loops

```move
public fun matrix_sum(matrix: vector<vector<u64>>): u64 {
    let sum = 0u64;
    let rows = vector::length(&matrix);
    
    for (i in 0..rows) {
        let row = vector::borrow(&matrix, i);
        let cols = vector::length(row);
        
        for (j in 0..cols) {
            let element = *vector::borrow(row, j);
            sum = sum + element;
        };
    };
    
    sum
}
```

## Match Statements

Match statements provide pattern matching capabilities, primarily used with enums. They allow you to execute different code based on the variant of an enum.

### Basic Match Statement

```move
module my_module::enums {
    enum Status {
        Active,
        Inactive,
        Pending,
    }
    
    public fun get_status_message(status: Status): String {
        match (status) {
            Status::Active => string::utf8(b"User is active"),
            Status::Inactive => string::utf8(b"User is inactive"),
            Status::Pending => string::utf8(b"User status is pending"),
        }
    }
}
```

### Match Statement with Data-Carrying Enums

```move
enum Result<T> {
    Ok(T),
    Err(String),
}

public fun handle_result(result: Result<u64>): String {
    match (result) {
        Result::Ok(value) => string::utf8(b"Success: ") + std::to_string(value),
        Result::Err(message) => string::utf8(b"Error: ") + message,
    }
}
```

### Match Statement with Complex Patterns

```move
enum Shape {
    Circle(u64),    // radius
    Rectangle(u64, u64), // width, height
    Square(u64),    // side
}

public fun calculate_area(shape: Shape): u64 {
    match (shape) {
        Shape::Circle(radius) => {
            // Approximate area calculation (π * r²)
            radius * radius * 3
        },
        Shape::Rectangle(width, height) => {
            width * height
        },
        Shape::Square(side) => {
            side * side
        },
    }
}
```

### Match Statement with Guards

```move
enum Number {
    Zero,
    Positive(u64),
    Negative(u64),
}

public fun classify_number(num: Number): String {
    match (num) {
        Number::Zero => string::utf8(b"Zero"),
        Number::Positive(value) => {
            if (value < 10) {
                string::utf8(b"Small positive")
            } else {
                string::utf8(b"Large positive")
            }
        },
        Number::Negative(value) => {
            if (value > 10) {
                string::utf8(b"Large negative")
            } else {
                string::utf8(b"Small negative")
            }
        },
    }
}
```

### Match Statement with Default Case

```move
enum Direction {
    North,
    South,
    East,
    West,
}

public fun get_direction_name(direction: Direction): String {
    match (direction) {
        Direction::North => string::utf8(b"North"),
        Direction::South => string::utf8(b"South"),
        Direction::East => string::utf8(b"East"),
        Direction::West => string::utf8(b"West"),
    }
}
```

### Match Statement in Error Handling

```move
enum ValidationResult {
    Valid,
    InvalidAge,
    InvalidName,
    InvalidEmail,
}

public fun validate_user(age: u64, name: String, email: String): ValidationResult {
    if (age < 18 || age > 120) {
        return ValidationResult::InvalidAge
    };
    
    if (string::length(&name) == 0) {
        return ValidationResult::InvalidName
    };
    
    if (string::length(&email) == 0) {
        return ValidationResult::InvalidEmail
    };
    
    ValidationResult::Valid
}

public fun get_validation_message(result: ValidationResult): String {
    match (result) {
        ValidationResult::Valid => string::utf8(b"User data is valid"),
        ValidationResult::InvalidAge => string::utf8(b"Age must be between 18 and 120"),
        ValidationResult::InvalidName => string::utf8(b"Name cannot be empty"),
        ValidationResult::InvalidEmail => string::utf8(b"Email cannot be empty"),
    }
}
```

## Best Practices

### If Statements

1. **Use early returns**: Return early to reduce nesting
2. **Keep conditions simple**: Break complex conditions into multiple if statements
3. **Use meaningful variable names**: Make conditions self-documenting

```move
// Good: Early return
public fun validate_input(input: u64): bool {
    if (input == 0) {
        return false
    };
    
    if (input > 1000) {
        return false
    };
    
    true
}

// Bad: Deep nesting
public fun validate_input_bad(input: u64): bool {
    if (input != 0) {
        if (input <= 1000) {
            return true
        } else {
            return false
        }
    } else {
        return false
    }
}
```

### While Loops

1. **Ensure termination**: Make sure loops will eventually terminate
2. **Use break for early exit**: Use break instead of complex conditions
3. **Initialize variables properly**: Initialize loop variables before the loop

```move
// Good: Clear termination condition
public fun safe_loop(max_iterations: u64): u64 {
    let i = 0;
    while (i < max_iterations) {
        i = i + 1;
    };
    i
}

// Bad: Potential infinite loop
public fun unsafe_loop(): u64 {
    let i = 0;
    while (i >= 0) { // This will never be false for u64
        i = i + 1;
    };
    i
}
```

### For Loops

1. **Use for loops for known ranges**: Prefer for loops when you know the iteration count
2. **Avoid modifying loop variables**: Don't modify the loop variable inside the loop
3. **Use meaningful variable names**: Use descriptive names for loop variables

```move
// Good: Clear iteration
public fun process_array(data: vector<u64>): u64 {
    let sum = 0u64;
    let len = vector::length(&data);
    
    for (index in 0..len) {
        let element = *vector::borrow(&data, index);
        sum = sum + element;
    };
    
    sum
}
```

### Match Statements

1. **Handle all cases**: Ensure all enum variants are covered
2. **Use meaningful patterns**: Use descriptive variable names in patterns
3. **Keep match arms simple**: Extract complex logic into separate functions

```move
// Good: All cases handled
public fun process_status(status: Status): String {
    match (status) {
        Status::Active => string::utf8(b"Active"),
        Status::Inactive => string::utf8(b"Inactive"),
        Status::Pending => string::utf8(b"Pending"),
    }
}

// Bad: Missing case (this would cause a compilation error)
public fun process_status_bad(status: Status): String {
    match (status) {
        Status::Active => string::utf8(b"Active"),
        Status::Inactive => string::utf8(b"Inactive"),
        // Missing Status::Pending case
    }
}
```

## Common Patterns

### Error Handling Pattern

```move
enum OperationResult {
    Success(u64),
    Failure(String),
}

public fun safe_divide(a: u64, b: u64): OperationResult {
    if (b == 0) {
        return OperationResult::Failure(string::utf8(b"Division by zero"))
    };
    
    OperationResult::Success(a / b)
}

public fun handle_division_result(result: OperationResult): String {
    match (result) {
        OperationResult::Success(value) => {
            string::utf8(b"Result: ") + std::to_string(value)
        },
        OperationResult::Failure(error) => {
            string::utf8(b"Error: ") + error
        },
    }
}
```

### State Machine Pattern

```move
enum GameState {
    Waiting,
    Playing,
    Paused,
    GameOver,
}

public fun update_game_state(current_state: GameState, action: String): GameState {
    match (current_state) {
        GameState::Waiting => {
            if (action == string::utf8(b"start")) {
                GameState::Playing
            } else {
                GameState::Waiting
            }
        },
        GameState::Playing => {
            if (action == string::utf8(b"pause")) {
                GameState::Paused
            } else if (action == string::utf8(b"end")) {
                GameState::GameOver
            } else {
                GameState::Playing
            }
        },
        GameState::Paused => {
            if (action == string::utf8(b"resume")) {
                GameState::Playing
            } else if (action == string::utf8(b"end")) {
                GameState::GameOver
            } else {
                GameState::Paused
            }
        },
        GameState::GameOver => GameState::GameOver,
    }
}
```

By understanding and using these control flow constructs effectively, you can write more expressive and maintainable Move code that handles complex logic and decision-making scenarios.
