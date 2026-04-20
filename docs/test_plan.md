# Test Plan
This is a basic test plan for the RoomLight prototype.
My goal is to check that the most important features work reliably, especially the logic that affects many rooms at once and the time-based automation.

## 1. What I Would Test
I would focus first on the core behavior.

1. Room type and profile configuration
- CRUD operations on room types and lighting profiles
- Assigning profiles to rooms

2. Controllpanels set light states correctly
- Both toggle and adjust controlls work correctly
- Targeting works both for labels and all lights

3. Time simulation
- Simulated clock advances correctly and fast forward buttons work
- Checkout and check-in events behave correctly

4. Persistence
- JSON files save data correctly
- Data should persist after restarts

## 2. How I Would Test
Since I am still learning testing, I would use a simple 3 layer approach.

1. Unit tests (main priority)
- Test model and system methods directly. There are plenty of decently complex logic that could easily break.

2. Integration tests
- Test flows across multiple classes
- Example: assign profile -> apply control -> light state changes

3. Manual testing
- Run the app and click through the UI to test "normal" flows

## 3. Why This Approach
I think this approach allows for a good balance between automation and human intuition.

- Unit tests catch logic bugs early
- Integration tests confirm classes work together
- Manual testing confirms the app as a whole works as intended


## 4. Main Risk Areas
If I had limited time, I would prioritize these risk areas:

1. Time simulatio bugs (easy to miss, easy to test automatically)
2. Data persistance (harder to automate, but agian easy to miss)
3. Core data and method "correctness" at unit test level (also allows catching regressions during development)

## 6. Exit Criteria (Simple)
I would consider testing good enough for demo if:

1. Core workflows run without crashes
2. Prototype equirements are verifiably demonstrated
3. Simulated check-in/check-out behavior works repeatedly
4. Saved data is still correct after restart