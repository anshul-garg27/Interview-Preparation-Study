"""
Elevator System - Demo
=======================
Demonstrates: State pattern (elevator states), Strategy pattern (scheduling),
multiple elevators, FCFS vs SCAN scheduling, and edge cases.

Run: cd code/ && python demo.py
"""

from request import Request
from fcfs_scheduler import FCFSScheduler
from scan_scheduler import SCANScheduler
from elevator_controller import ElevatorController
from building import Building


if __name__ == "__main__":
    print("=" * 60)
    print("  ELEVATOR SYSTEM - Modular LLD Demo")
    print("=" * 60)

    # ---- Scenario 1: FCFS Strategy ----
    print("\n[Scenario 1: FCFS Strategy with 2 Elevators]")
    building1 = Building("Tower A", num_floors=10, num_elevators=2, strategy=FCFSScheduler())
    ctrl1 = building1.controller
    ctrl1.display_status()

    ctrl1.request_elevator(Request(source_floor=0, destination_floor=5))
    ctrl1.request_elevator(Request(source_floor=3, destination_floor=7))
    ctrl1.request_elevator(Request(source_floor=8, destination_floor=1))

    print("\n  --- Running Simulation ---")
    ctrl1.simulate()
    ctrl1.display_status()

    # ---- Scenario 2: SCAN Strategy ----
    print("\n" + "=" * 60)
    print("[Scenario 2: SCAN Strategy with 3 Elevators]")
    Request.reset_counter()
    ctrl2 = ElevatorController(num_elevators=3, num_floors=15, strategy=SCANScheduler())

    # Pre-position elevators at different floors
    ctrl2.elevators[0].current_floor = 2
    ctrl2.elevators[1].current_floor = 7
    ctrl2.elevators[2].current_floor = 12
    ctrl2.display_status()

    requests = [
        Request(3, 9),    # Near elevator at floor 2
        Request(6, 1),    # Near elevator at floor 7
        Request(14, 5),   # Near elevator at floor 12
        Request(1, 10),   # Should go to nearest idle
        Request(8, 3),
    ]
    for r in requests:
        ctrl2.request_elevator(r)

    print("\n  --- Running Simulation ---")
    ctrl2.simulate(max_steps=60)
    ctrl2.display_status()

    # ---- Scenario 3: Edge Case - Same Floor Request ----
    print("\n" + "=" * 60)
    print("[Scenario 3: Edge Case - Request from Same Floor]")
    Request.reset_counter()
    ctrl3 = ElevatorController(num_elevators=1, num_floors=5)
    ctrl3.elevators[0].current_floor = 3
    ctrl3.request_elevator(Request(3, 5))
    ctrl3.simulate()
    ctrl3.display_status()

    # ---- Scenario 4: Building with strategy swap ----
    print("\n" + "=" * 60)
    print("[Scenario 4: Dynamic Strategy Swap]")
    Request.reset_counter()
    building2 = Building("Tower B", num_floors=10, num_elevators=2)
    ctrl4 = building2.controller
    print(f"  {building2}")

    ctrl4.request_elevator(Request(0, 8))
    print("  -- Swapping to SCAN strategy --")
    ctrl4.set_strategy(SCANScheduler())
    ctrl4.request_elevator(Request(5, 1))

    ctrl4.simulate()
    ctrl4.display_status()

    print("\nDemo complete!")
