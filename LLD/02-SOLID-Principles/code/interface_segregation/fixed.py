"""ISP Fixed - Small, focused interfaces. Implement only what you need."""

from abc import ABC, abstractmethod


class Workable(ABC):
    @abstractmethod
    def work(self) -> str:
        pass


class Eatable(ABC):
    @abstractmethod
    def eat(self) -> str:
        pass


class Sleepable(ABC):
    @abstractmethod
    def sleep(self) -> str:
        pass


class Meetable(ABC):
    @abstractmethod
    def attend_meeting(self) -> str:
        pass


class HumanWorker(Workable, Eatable, Sleepable, Meetable):
    """Human implements ALL interfaces - that's fine, humans do all these."""

    def work(self) -> str:
        return "Human writing code"

    def eat(self) -> str:
        return "Human having lunch"

    def sleep(self) -> str:
        return "Human sleeping 8 hours"

    def attend_meeting(self) -> str:
        return "Human in standup meeting"


class RobotWorker(Workable):
    """Robot ONLY implements Workable - no eat/sleep/meeting nonsense."""

    def work(self) -> str:
        return "Robot assembling parts 24/7"


class InternWorker(Workable, Eatable, Meetable):
    """Intern works, eats, and attends meetings (but no sleeping on the job!)."""

    def work(self) -> str:
        return "Intern learning and coding"

    def eat(self) -> str:
        return "Intern eating free snacks"

    def attend_meeting(self) -> str:
        return "Intern observing meeting"


def do_work(workers: list[Workable]) -> None:
    """Only cares about Workable - works with any worker type."""
    for w in workers:
        print(f"  {w.__class__.__name__}: {w.work()}")


if __name__ == "__main__":
    print("GOOD DESIGN: Interface Segregation Principle\n")

    all_workers: list[Workable] = [HumanWorker(), RobotWorker(), InternWorker()]
    do_work(all_workers)

    print("\nFeeding time (only Eatable workers):")
    eaters = [w for w in all_workers if isinstance(w, Eatable)]
    for e in eaters:
        print(f"  {e.__class__.__name__}: {e.eat()}")

    print("\nBENEFITS:")
    print("  1. Robot doesn't implement eat() or sleep()")
    print("  2. Each interface is small and focused")
    print("  3. Classes implement ONLY relevant interfaces")
    print("  4. No NotImplementedError anywhere")
