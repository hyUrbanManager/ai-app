document.addEventListener('DOMContentLoaded', function() {
    const result = document.getElementById('result');
    const buttons = document.querySelectorAll('button');
    
    let currentInput = '';
    let currentOperation = null;
    let previousInput = '';
    
    // Add event listeners to all buttons
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const value = this.textContent;
            
            // Handle different button types
            if (value === 'C') {
                clear();
            } else if (value === 'DEL') {
                deleteLastChar();
            } else if (value === '=') {
                calculate();
            } else if (['+', '-', '×', '÷', '%'].includes(value)) {
                handleOperator(value);
            } else {
                appendNumber(value);
            }
            
            updateDisplay();
        });
    });
    
    // Clear all values
    function clear() {
        currentInput = '';
        previousInput = '';
        currentOperation = null;
    }
    
    // Delete the last character
    function deleteLastChar() {
        currentInput = currentInput.toString().slice(0, -1);
    }
    
    // Append a number to the current input
    function appendNumber(number) {
        // Prevent multiple decimal points
        if (number === '.' && currentInput.includes('.')) return;
        
        // Limit the length of input to prevent overflow
        if (currentInput.length < 12) {
            currentInput = currentInput.toString() + number.toString();
        }
    }
    
    // Handle operator buttons
    function handleOperator(operator) {
        if (currentInput === '') return;
        
        if (previousInput !== '') {
            calculate();
        }
        
        currentOperation = operator;
        previousInput = currentInput;
        currentInput = '';
    }
    
    // Perform calculation
    function calculate() {
        if (currentOperation === null || previousInput === '' || currentInput === '') return;
        
        let computation;
        const prev = parseFloat(previousInput);
        const current = parseFloat(currentInput);
        
        if (isNaN(prev) || isNaN(current)) return;
        
        switch (currentOperation) {
            case '+':
                computation = prev + current;
                break;
            case '-':
                computation = prev - current;
                break;
            case '×':
                computation = prev * current;
                break;
            case '÷':
                if (current === 0) {
                    alert('除数不能为零！');
                    clear();
                    return;
                }
                computation = prev / current;
                break;
            case '%':
                computation = prev % current;
                break;
            default:
                return;
        }
        
        // Round to avoid floating point issues and limit to 12 digits
        computation = Math.round(computation * 1000000000000) / 1000000000000;
        
        // Convert to string and limit length
        currentInput = computation.toString().slice(0, 12);
        currentOperation = null;
        previousInput = '';
    }
    
    // Update the display
    function updateDisplay() {
        result.value = currentInput;
    }
    
    // Initialize display
    updateDisplay();
    
    // Add keyboard support
    document.addEventListener('keydown', function(event) {
        const key = event.key;
        
        // Numbers 0-9 and decimal point
        if (/^[0-9.]$/.test(key)) {
            appendNumber(key);
            updateDisplay();
            return;
        }
        
        // Operators
        switch (key) {
            case '+':
                handleOperator('+');
                break;
            case '-':
                handleOperator('-');
                break;
            case '*':
                handleOperator('×');
                break;
            case '/':
                handleOperator('÷');
                break;
            case '%':
                handleOperator('%');
                break;
            case 'Enter':
                calculate();
                break;
            case 'Backspace':
                deleteLastChar();
                break;
            case 'Escape':
                clear();
                break;
            default:
                return;
        }
        
        updateDisplay();
    });
});
