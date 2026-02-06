"""ISP Violation - Fat interface forces classes to implement irrelevant methods."""

from abc import ABC, abstractmethod


class Worker(ABC):
    """BAD: One fat interface for ALL worker types."""

    @abstractmethod
    def work(self) -> str:
        pass

    @abstractmethod
    def eat(self) -> str:
        pass

    @abstractmethod
    def sleep(self) -> str:
        pass

    @abstractmethod
    def attend_meeting(self) -> str:
        pass


class HumanWorker(Worker):
    """Fine - humans do all of these."""

    def work(self) -> str:
        return "Human working on code"

    def eat(self) -> str:
        return "Human eating lunch"

    def sleep(self) -> str:
        return "Human sleeping"

    def attend_meeting(self) -> str:
        return "Human in meeting"


class RobotWorker(Worker):
    """BAD: Robot doesn't eat or sleep, but MUST implement these methods."""

    def work(self) -> str:
        return "Robot assembling parts"

    def eat(self) -> str:
        raise NotImplementedError("Robots don't eat!")  # Forced empty implementation

    def sleep(self) -> str:
        raise NotImplementedError("Robots don't sleep!")

    def attend_meeting(self) -> str:
        raise NotImplementedError("Robots don't attend meetings!")


if __name__ == "__main__":
    print("BAD DESIGN: Interface Segregation Violation\n")

    human = HumanWorker()
    robot = RobotWorker()

    print("Human:")
    print(f"  {human.work()}")
    print(f"  {human.eat()}")

    print("\nRobot:")
    print(f"  {robot.work()}")
    try:
        robot.eat()
    except NotImplementedError as e:
        print(f"  eat() -> ERROR: {e}")
    try:
        robot.sleep()
    except NotImplementedError as e:
        print(f"  sleep() -> ERROR: {e}")

    print("\nPROBLEMS:")
    print("  1. Robot forced to implement eat(), sleep(), attend_meeting()")
    print("  2. Callers must handle NotImplementedError for robots")
    print("  3. Fat interface grows as new methods are added")
    print("  4. Every implementor gets burdened with irrelevant methods")
