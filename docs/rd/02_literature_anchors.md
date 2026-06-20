# Literature Anchors for CAK R&D

This note is concise and non-exhaustive. It records design anchors for CAK R&D;
it does not claim that these systems directly solve CAK's problem.

## Voyager

- Uses executable code skills.
- Performs self-verification before adding a skill to the library.
- Maintains an external skill library without weight updates.
- Reuses skills compositionally.
- Shows transfer to a new world / another agent can benefit from the skill library.
- Limitation: assumes stable API/environment feedback.

## AWM

- Induces workflow memory from trajectories.
- Supports offline and online induction.
- Shows that abstract sub-routines can be better than raw examples.
- Finds that workflow-actions only modestly help and can be brittle in dynamic UI.
- Key lesson: workflow representation needs runtime state awareness.

## HASP

- Treats skills as executable Program Functions, not passive advice.
- Uses a `should_activate` + `intervene` interface.
- Supports action override and context injection.
- Produces structured intervention records for training.
- Controls skill evolution with executable validation and teacher review.
- Shows that strict filtering is necessary to avoid library pollution.

## Implications for CAK

- CAK should study skills as runtime-control objects, not just memory records.
- CAK should not assume one universal skill format.
- CAK should require verifier/replay/admission for active skills.
- CAK should treat protocol extraction as a later step.
