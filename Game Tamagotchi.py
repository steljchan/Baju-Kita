import random

print("Welcome to Tamagotchi Game!")
name = input("Enter a name for your pet: ").strip()

health = 5
hungry = 2
mood = 2
clean = 4

lastChoice = None
count = 0
while health > 0:
    print(f"\n=== {name}'s Status ===")
    print(f"Health: {health}")
    print(f"Hungry: {hungry}")
    print(f"Mood: {mood}")
    print(f"Clean: {clean}")

    print("\nWhat would you like to do?")
    print("1. Eat")
    print("2. Bath")
    print("3. Play")
    print("4. Sleep")
    print("5. Exit")
    
    choice = int(input("Enter your choice: "))

    if choice == lastChoice and choice != 3:
        count += 1
    else:
        count = 0  
    lastChoice = choice

    if count > 3:
        health -= 1
        print(f"{name} is getting bored of doing the same thing! Health -1.")

    if choice == 1:
        hungry += 2
        if hungry > 5 or hungry < 1:
            health -= 1
        hungry = max(1, min(5, hungry))
        print(f"{name} enjoyed the meal!")
        
    
    elif choice == 2:
        clean = 5
        mood -= 1
        if mood > 5 or mood < 1:
            health -= 1
        mood = max(1, min(5, mood))
        print(f"{name} is now clean!")
    
    elif choice == 3: 
        while hungry > 1:
            print(f"\n=== {name}'s Status ===")
            print(f"Health: {health}")
            print(f"Hungry: {hungry}")
            print(f"Mood: {mood}")
            print(f"Clean: {clean}")
            print("\nWhat game do you want to play?")
            print("1. Guess The Word")
            print("2. Guess The Boom Number")
            print("3. Guess The Character")
            print("4. Exit Play")
            game = int(input("Choose a game: "))
            if game == 1:
                words = ["eat", "sleep", "game", "alpro", "vale", "stella", "dino", "nata", "aurel", "gerar",  
                         "vivi", "gladys", "love", "amd", "bear", "pink", "blue", "kill", "sun", "moon",
                         "star", "play", "bath", "study", "eyes", "nose", "lips", "cat", "ears", "world"]
                chosenWord = random.choice(words)
                guess = ["_"] * len(chosenWord)
                attempts = 7
                print("\nGuess the word! Enter one letter at a time.")
                print("You have 7 attempts to guess the word.")

                while attempts > 0 and "_" in guess:
                    print("Word so far: " + " ".join(guess))
                    letter = input("Enter a letter: ").strip().lower()
                    if len(letter) != 1 or not letter.isalpha():
                        print("Please enter a single valid letter.")
                        continue
                    if letter in chosenWord: 
                        for i, char in enumerate(chosenWord):
                            if char == letter:
                                guess[i] = letter 
                                print(f"Good guess! The letter '{letter}' is in the word.")
                    else:
                        attempts -= 1
                        print(f"Wrong guess! The letter '{letter}' is not in the word. Attempts left: {attempts}")
                if "_" not in guess:
                    mood += 1
                    print(f"Congratulations! You guessed the word: {''.join(guess)}")
                else:
                    mood -= 1
                    print(f"Out of attempts! The correct word was: {chosenWord}.")
                clean -= 1
                hungry -= 1

            
            elif game == 2:
                print("Guess a number between 1 and 100. Find the bomb!")
                bomb = random.randint(1, 100) 
                attempts = 10 
                while attempts > 0:
                    try:
                        guess = int(input("Enter your guess: ").strip())
                        if guess < 1 or guess > 100:
                            print("Please enter a number between 1 and 100.")
                            continue
                        if guess == bomb:
                            print(f"Wow! You got the bomb number {bomb}. Congratulations!")
                            mood += 1
                            break
                        elif guess < bomb:
                            print("Too low!")
                        elif guess > bomb:
                            print("Too high!")
                        attempts -= 1
                        if attempts > 0:
                            print(f"You have {attempts} attempts left.")
                        else:
                            print(f"Out of attempts! The bomb was at {bomb}.")
                            mood -= 1
                    except ValueError:
                        print("Please enter a valid number.")
                clean -= 1
                hungry -= 1
            
            elif game == 3:
                characters = {"Harry Potter": "A young wizard who attends Hogwarts School of Witchcraft and Wizardry.",
                            "Luke Skywalker": "The protagonist of Star Wars, a Jedi Knight and the son of Anakin Skywalker.",
                            "Sherlock Holmes": "A famous detective known for solving complex cases using logical reasoning.",
                            "Wonder Woman": "A superheroine from DC Comics, known for her strength and compassion.",
                            "Iron Man": "A billionaire playboy, philanthropist, and genius inventor who becomes a superhero.",
                            "Batman": "A billionaire who fights crime in Gotham City using his physical prowess and intellect.",
                            "Spider-Man": "A teenage superhero bitten by a radioactive spider, gaining the ability to climb walls.",
                            "Hermione Granger": "One of Harry Potter's best friends, a highly intelligent witch from the Harry Potter series.",
                            "Gandalf": "A wizard from 'The Lord of the Rings,' known for his wisdom and magical powers.",
                            "Daenerys Targaryen": "A character from 'Game of Thrones,' known as the Mother of Dragons.",
                            "Jon Snow": "A character from 'Game of Thrones,' known for his bravery and being the Lord Commander of the Night's Watch.",
                            "Captain America": "A super soldier from Marvel Comics, known for his shield and his fight against Hydra.",
                            "The Hulk": "A scientist who transforms into a giant, green-skinned superhero when angry.",
                            "Black Widow": "A highly skilled spy and former assassin, known for her agility and combat skills.",
                            "Thor": "A Norse god of thunder and a superhero from Marvel Comics, wielding a hammer called Mjolnir.",
                            "Aquaman": "A superhero and king of Atlantis, who can communicate with sea creatures.",
                            "The Flash": "A superhero known for his super speed, part of the Justice League.",
                            "Deadpool": "A wisecracking antihero with regenerative healing abilities.",
                            "Loki": "The Norse god of mischief, often portrayed as a villain in Marvel Comics.",
                            "The Joker": "A psychotic villain from Batman's rogues gallery, known for his clownish appearance.",
                            "Wolverine": "A mutant with healing abilities and retractable claws, known for his animalistic nature.",
                            "Magneto": "A powerful mutant with the ability to control metal, often a villain in X-Men comics.",
                            "Professor X": "The leader of the X-Men, with the ability to read and control minds.",
                            "Hannibal Lecter": "A fictional psychiatrist and cannibalistic serial killer in popular fiction.",
                            "Voldemort": "The dark wizard from Harry Potter who seeks to conquer the magical world."}
                character, hint = random.choice(list(characters.items()))
                attempts = 3  
                print("Welcome to the Quiz: Guess the Character!")
                print(f"Hint: {hint}")
                while attempts > 0:
                    guess = input("Enter your guess: ").strip().lower()
                    if guess == character.lower():
                        mood += 1 
                        print(f"Correct! The character was {character}.")
                        break
                    else:
                        attempts -= 1
                        if attempts > 0:
                            print(f"Incorrect! You have {attempts} attempts left.")
                        else:
                            print(f"Out of attempts! The character was {character}.")
                            mood -= 1
                if attempts > 0:
                    print(f"Good job!")
                else:
                    print(f"Better luck next time!")
                clean -= 1
                hungry -= 1

            elif game == 4:
                print("{name} had fun playing!")
                break

            else:
                print("Invalid game choice. No game played.")
            if hungry <= 1 or clean <= 1:
                if hungry <= 1:
                    print(f"{name} had fun playing! Now {name} is hungry. It's time to eat!")
                elif hungry <= 1 or clean <= 1:
                    print(f"{name} had fun playing! Now {name} is hungry and dirty.") 
                else:
                    print(f"{name} had fun playing! Now {name} is dirty. It's time to take a bath!")
            if mood > 5 or mood < 1 or clean > 5 or clean < 1 or hungry > 5 or hungry < 1:
                health -= 1

            mood = max(1, min(5, mood))
            clean = max(1, min(5, clean))
            hungry = max(1, min(5, hungry))
            
        if game != 4:
            count += 1

    elif choice == 4:
        health += 1
        hungry -= 2
        if hungry > 5 or hungry < 1:
            health -= 1
        hungry = max(1, min(5, hungry))
        health = max(0, min(5, health))


        print(f"{name} took a nap!")

    elif choice == 5: 
        print(f"Goodbye! {name} will miss you!")
        break
    
    else:
        print("Invalid choice. Please try again.")
    if health <= 0:
        print(f"Oh no! {name}'s health has reached 0. Game Over!")