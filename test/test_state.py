from state_manager import (
    save_state,
    get_state,
    clear_state
)

save_state(
    "123",
    "waiting_service",
    {}
)

print(
    get_state("123")
)

clear_state("123")

print(
    get_state("123")
)