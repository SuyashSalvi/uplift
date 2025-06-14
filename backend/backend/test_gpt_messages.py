from gpt_utils import gpt_generator

def test_message_generation():
    print("\n=== Testing GPT Message Generation ===\n")
    
    # Test meal messages
    print("Testing Meal Messages:")
    print("-" * 50)
    for i in range(3):
        message = gpt_generator.generate_motivational_message("meal")
        print(f"Meal Message {i+1}: {message}")
        print(f"Length: {len(message)} characters")
        print("-" * 50)
    
    # Test workout messages
    print("\nTesting Workout Messages:")
    print("-" * 50)
    for i in range(3):
        message = gpt_generator.generate_motivational_message("workout")
        print(f"Workout Message {i+1}: {message}")
        print(f"Length: {len(message)} characters")
        print("-" * 50)
    
    # Test user reply generation
    print("\nTesting User Reply Generation:")
    print("-" * 50)
    test_replies = [
        "I'm feeling tired today",
        "Just completed my workout!",
        "Can't find motivation to eat healthy"
    ]
    
    for reply in test_replies:
        response = gpt_generator.generate_reply_to_user(reply)
        print(f"User: {reply}")
        print(f"GPT: {response}")
        print(f"Length: {len(response)} characters")
        print("-" * 50)

if __name__ == "__main__":
    test_message_generation() 