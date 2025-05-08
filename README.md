# Your-own-adventure-gamemaster

## Remarks

- It seems mandatory to give demonstrations to the agent, otherwise it just doesn't format its output well.
- Demonstrations shouldn't include "Start the game" otherwise it's orentating too much the first input. Avoid giving names of places as well, which you would probably end up retrieving in the outputs.

- [x] The hardest part is to get the chatbot to write a proper story, it's always going for a basic fantasy story.
    * Seems to have been fixed by:
      * Creating an agent
      * Providing some instructions
      * Providing some demonstrations
    * The problem now is that it's overfit on "Take left/take right" options
    * Also sometimes saying "1. You take right" at the beginning of the message, probably mixing up repeating user choice and suggestions at the end of the message.
- [x] Maybe we should refactor the following way:
    * The user has access to buttons that match the suggested choices from the agent.
    * Clicking on a button doesn't send the index, but the choice's text itself.
- [ ] Need to train on way more data, the outputs are too limited for now, sounds like a kid trying to imitate a good writer's style.
- [ ] Sometimes the actions suggested are not formatted properly.
- [ ] Maybe should set a "window" for the context to avoid sending too much data after many messages.
