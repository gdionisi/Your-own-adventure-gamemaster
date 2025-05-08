# Your-own-adventure-gamemaster

## Remarks

* The hardest part is to get the chatbot to write a proper story, it's always going for a basic fantasy story.
  * Seems to have been fixed by:
    * Creating an agent
    * Providing some instructions
    * Providing some demonstrations
  * The problem now is that it's overfit on "Take left/take right" options
  * Also sometimes saying "1. You take right" at the beginning of the message, probably mixing up repeating user choice and suggestions at the end of the message.