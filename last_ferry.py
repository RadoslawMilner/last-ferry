"""A tiny stateful RPG encounter about a disputed ferry crossing."""

from dataclasses import dataclass


@dataclass
class EncounterState:
    heard_nessas_reason: bool = False
    found_authorization: bool = False
    bram_agreed_to_help: bool = False
    finished: bool = False


def print_tip(choices: str) -> None:
    print(f"Enter {choices}, or type 'exit' to quit.")


def exit_game(state: EncounterState) -> None:
    print("\nYou leave the encounter. Goodbye.")
    state.finished = True


def show_scene() -> None:
    print("""
                  RIVER / FERRY
               [Bram at the rope]
                 about 5 paces
                       |
    [Nessa + sealed crate] -- [Ledger on a stand]
          about 2 paces
                       |
                [YOU, dock entrance]
    """)
    print("Nessa and Bram are within talking distance. Use options 1 and 3 to speak with them.")


def talk_to_nessa(state: EncounterState) -> None:
    if state.heard_nessas_reason:
        print("Nessa: The hamlet has been cut off by the flood. They need this medicine tonight.")
        return

    print("Nessa: The hamlet across the river is cut off by the flood. The medicine in that crate is for them.")
    state.heard_nessas_reason = True


def inspect_ledger(state: EncounterState) -> None:
    if state.found_authorization:
        print("You check the ledger again. The authorization is still there, under the torn page.")
        return

    print("You lift a torn page and find a stamped authorization for Nessa's medicine crate.")
    state.found_authorization = True


def talk_to_bram(state: EncounterState) -> None:
    if state.bram_agreed_to_help:
        print("Bram: I'll take the risk. Choose quickly; the watch is coming back.")
        return

    if state.heard_nessas_reason and state.found_authorization:
        print("Bram: You have a reason and proof. I'll distract the watch if you choose to hide the crate.")
        state.bram_agreed_to_help = True
        return

    missing = []
    if not state.heard_nessas_reason:
        missing.append("why the medicine matters")
    if not state.found_authorization:
        missing.append("proof that it is allowed")
    print(f"Bram: I won't risk my ferry without { ' and '.join(missing) }.")


def make_a_plan(state: EncounterState) -> None:
    print("\nChoose your plan:")
    print("1. Show the authorization to the watch")
    print("2. Hide the crate and sail now")
    print("3. Leave the crate behind")
    print("b. Return to the dock")
    print_tip("1, 2, 3, or b")

    choice = input("> ").strip().lower()

    if choice == "exit":
        exit_game(state)
    elif choice == "1":
        if state.found_authorization:
            print("\nThe watch verifies the stamp. Nessa boards openly, and the medicine reaches the hamlet.")
        else:
            print("\nWithout a record, the watch holds the crate for inspection. Nessa misses the crossing.")
        state.finished = True
    elif choice == "2":
        if state.bram_agreed_to_help:
            print("\nBram draws the watch away. The ferry slips across with the crate, but his license is now at risk.")
        else:
            print("\nThe watch spots the crate. Nessa is detained, and Bram loses his ferry license.")
        state.finished = True
    elif choice == "3":
        print("\nYou leave the crate at the dock. The ferry departs without Nessa or the medicine.")
        state.finished = True
    elif choice == "b":
        return
    else:
        print("That option isn't on the plan menu. You return to the dock.")


def show_state(state: EncounterState) -> None:
    reason = "learned" if state.heard_nessas_reason else "unknown"
    authorization = "found" if state.found_authorization else "not found"
    help_status = "agreed" if state.bram_agreed_to_help else "not agreed"
    print(f"\nYour notes:\nNessa's reason: {reason}.\nauthorization: {authorization}.\nBram's help: {help_status}.")


def main() -> None:
    state = EncounterState()

    print("THE LAST FERRY")
    print("\nROLE: You are the envoy of a hamlet cut off by floodwater.")
    print("GOAL: Help Nessa get her medicine crate across the river before the storm closes the ferry.")
    print("The ferry watch has flagged the crate as undeclared. Learn what happened, then choose how to cross.")
    show_scene()

    while not state.finished:
        show_state(state)
        print("\n1. Talk to Nessa")
        print("2. Inspect the cargo ledger")
        print("3. Talk to Bram")
        print("4. Make a plan")
        print("5. Leave the dock")
        print_tip("1-5")

        choice = input("> ").strip()

        if choice.lower() == "exit":
            exit_game(state)
        elif choice == "1":
            talk_to_nessa(state)
        elif choice == "2":
            inspect_ledger(state)
        elif choice == "3":
            talk_to_bram(state)
        elif choice == "4":
            make_a_plan(state)
        elif choice == "5":
            print("\nYou leave the dock. The ferry departs without the medicine.")
            state.finished = True
        else:
            print("That option isn't on the dock menu.")
            print_tip("1-5")


if __name__ == "__main__":
    main()
