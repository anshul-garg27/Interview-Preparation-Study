"""
Stack Overflow / Q&A Forum - Low Level Design
Run: python stackoverflow.py

Patterns: Observer (reputation), Strategy (search), State (question status),
          Composite (commentable posts)
Key: Reputation system, voting rules, search ranking
"""
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import uuid


# ─── Badge System ────────────────────────────────────────────────────
class BadgeLevel(Enum):
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"


class Badge:
    def __init__(self, name: str, description: str, level: BadgeLevel):
        self.name = name
        self.description = description
        self.level = level

    def __repr__(self):
        return f"[{self.level.value}] {self.name}"


# ─── User ────────────────────────────────────────────────────────────
class User:
    UPVOTE_REP = 15
    DOWNVOTE_REP = 125
    COMMENT_REP = 50

    def __init__(self, username: str, email: str):
        self.id = str(uuid.uuid4())[:6]
        self.username = username
        self.email = email
        self.reputation = 1
        self.badges: list[Badge] = []
        self.joined_at = datetime.now()

    def can_upvote(self) -> bool:
        return self.reputation >= self.UPVOTE_REP

    def can_downvote(self) -> bool:
        return self.reputation >= self.DOWNVOTE_REP

    def can_comment(self) -> bool:
        return self.reputation >= self.COMMENT_REP

    def add_reputation(self, amount: int):
        self.reputation = max(1, self.reputation + amount)

    def award_badge(self, badge: Badge):
        if badge.name not in [b.name for b in self.badges]:
            self.badges.append(badge)
            print(f"    [Badge] {self.username} earned: {badge}")

    def __repr__(self):
        return f"{self.username} (rep: {self.reputation})"


# ─── Comments ────────────────────────────────────────────────────────
class Comment:
    def __init__(self, author: User, text: str):
        self.id = str(uuid.uuid4())[:6]
        self.author = author
        self.text = text
        self.created_at = datetime.now()

    def __repr__(self):
        return f"  Comment by {self.author.username}: {self.text[:50]}"


# ─── State Pattern: Question Status ─────────────────────────────────
class QuestionState(ABC):
    @abstractmethod
    def get_name(self) -> str: pass
    def can_answer(self) -> bool: return False
    def can_close(self) -> bool: return False
    def can_reopen(self) -> bool: return False


class OpenState(QuestionState):
    def get_name(self): return "Open"
    def can_answer(self): return True
    def can_close(self): return True


class ClosedState(QuestionState):
    def __init__(self, reason: str = ""):
        self.reason = reason
    def get_name(self): return f"Closed ({self.reason})"
    def can_reopen(self): return True


# ─── Posts (Abstract base for Question and Answer) ───────────────────
class Post(ABC):
    def __init__(self, author: User, body: str):
        self.id = str(uuid.uuid4())[:6]
        self.author = author
        self.body = body
        self.created_at = datetime.now()
        self.comments: list[Comment] = []
        self._votes: dict[str, int] = {}  # user_id -> +1 or -1

    @property
    def score(self) -> int:
        return sum(self._votes.values())

    def vote(self, user: User, value: int) -> int | None:
        """Vote on this post. Returns the net change or None if invalid."""
        if user.id == self.author.id:
            raise ValueError("Cannot vote on your own post")
        old_vote = self._votes.get(user.id, 0)
        if old_vote == value:
            # Undo vote
            del self._votes[user.id]
            return -value
        else:
            self._votes[user.id] = value
            return value - old_vote

    def add_comment(self, comment: Comment):
        self.comments.append(comment)


class Question(Post):
    def __init__(self, author: User, title: str, body: str,
                 tags: list[str]):
        super().__init__(author, body)
        self.title = title
        self.tags = tags
        self.answers: list["Answer"] = []
        self.accepted_answer: "Answer | None" = None
        self.state: QuestionState = OpenState()

    def add_answer(self, answer: "Answer"):
        if not self.state.can_answer():
            raise ValueError(f"Cannot answer a {self.state.get_name()} question")
        self.answers.append(answer)

    def accept_answer(self, answer: "Answer", user: User):
        if user.id != self.author.id:
            raise ValueError("Only the question author can accept an answer")
        if self.accepted_answer:
            self.accepted_answer.is_accepted = False
        answer.is_accepted = True
        self.accepted_answer = answer

    def close(self, reason: str):
        if not self.state.can_close():
            raise ValueError("Cannot close this question")
        self.state = ClosedState(reason)

    def reopen(self):
        if not self.state.can_reopen():
            raise ValueError("Cannot reopen this question")
        self.state = OpenState()

    def __repr__(self):
        return (f"Q: {self.title} [score={self.score}, "
                f"answers={len(self.answers)}, {self.state.get_name()}]")


class Answer(Post):
    def __init__(self, author: User, question: Question, body: str):
        super().__init__(author, body)
        self.question = question
        self.is_accepted = False

    def __repr__(self):
        acc = " [ACCEPTED]" if self.is_accepted else ""
        return f"A by {self.author.username} [score={self.score}]{acc}"


# ─── Observer: Reputation ────────────────────────────────────────────
class ReputationObserver(ABC):
    @abstractmethod
    def on_vote(self, post: Post, voter: User, net_change: int):
        pass

    @abstractmethod
    def on_accept(self, answer: Answer, asker: User):
        pass


class ReputationManager(ReputationObserver):
    QUESTION_UPVOTE = 10
    ANSWER_UPVOTE = 10
    DOWNVOTE_RECEIVED = -2
    DOWNVOTE_COST = -1
    ACCEPT_ANSWERER = 15
    ACCEPT_ASKER = 2

    def __init__(self):
        self._badges = {
            "First Question": Badge("First Question", "Asked first question", BadgeLevel.BRONZE),
            "First Answer": Badge("First Answer", "Posted first answer", BadgeLevel.BRONZE),
            "Nice Answer": Badge("Nice Answer", "Answer score of 10+", BadgeLevel.BRONZE),
            "Good Answer": Badge("Good Answer", "Answer score of 25+", BadgeLevel.SILVER),
            "Great Answer": Badge("Great Answer", "Answer score of 100+", BadgeLevel.GOLD),
            "Critic": Badge("Critic", "First downvote", BadgeLevel.BRONZE),
        }

    def on_vote(self, post: Post, voter: User, net_change: int):
        if net_change > 0:  # upvote
            post.author.add_reputation(
                self.ANSWER_UPVOTE if isinstance(post, Answer)
                else self.QUESTION_UPVOTE)
        elif net_change < 0:  # downvote
            post.author.add_reputation(self.DOWNVOTE_RECEIVED)
            voter.add_reputation(self.DOWNVOTE_COST)
            voter.award_badge(self._badges["Critic"])

        # Check badges
        if isinstance(post, Answer) and post.score >= 10:
            post.author.award_badge(self._badges["Nice Answer"])

    def on_accept(self, answer: Answer, asker: User):
        # Don't give rep for accepting own answer
        if answer.author.id != asker.id:
            answer.author.add_reputation(self.ACCEPT_ANSWERER)
            asker.add_reputation(self.ACCEPT_ASKER)


# ─── Strategy: Search ────────────────────────────────────────────────
class SearchStrategy(ABC):
    @abstractmethod
    def search(self, query: str,
               questions: list[Question]) -> list[Question]:
        pass


class RelevanceSearch(SearchStrategy):
    """Score by keyword match in title + tags + vote score."""
    def search(self, query, questions):
        terms = query.lower().split()
        scored = []
        for q in questions:
            score = 0
            text = (q.title + " " + " ".join(q.tags)).lower()
            for term in terms:
                if term in text:
                    score += 10
            score += q.score  # boost by votes
            if q.accepted_answer:
                score += 5  # boost if has accepted answer
            if score > 0:
                scored.append((score, q))
        scored.sort(key=lambda x: -x[0])
        return [q for _, q in scored]


class MostVotedSearch(SearchStrategy):
    """Filter by query, sort by vote score."""
    def search(self, query, questions):
        terms = query.lower().split()
        matches = [q for q in questions
                   if any(t in (q.title + " ".join(q.tags)).lower()
                          for t in terms)]
        return sorted(matches, key=lambda q: -q.score)


# ─── Service ─────────────────────────────────────────────────────────
class QAService:
    def __init__(self):
        self.users: dict[str, User] = {}
        self.questions: dict[str, Question] = {}
        self.observers: list[ReputationObserver] = []
        self.search_strategy: SearchStrategy = RelevanceSearch()

    def add_observer(self, obs: ReputationObserver):
        self.observers.append(obs)

    def register_user(self, username: str, email: str) -> User:
        user = User(username, email)
        # Give enough rep to test all features
        user.reputation = 200
        self.users[user.id] = user
        return user

    def post_question(self, user: User, title: str, body: str,
                      tags: list[str]) -> Question:
        q = Question(user, title, body, tags)
        self.questions[q.id] = q
        return q

    def post_answer(self, user: User, question: Question,
                    body: str) -> Answer:
        answer = Answer(user, question, body)
        question.add_answer(answer)
        return answer

    def vote(self, user: User, post: Post, is_upvote: bool):
        value = 1 if is_upvote else -1
        if is_upvote and not user.can_upvote():
            raise PermissionError(f"Need {User.UPVOTE_REP} rep to upvote")
        if not is_upvote and not user.can_downvote():
            raise PermissionError(f"Need {User.DOWNVOTE_REP} rep to downvote")
        net = post.vote(user, value)
        if net:
            for obs in self.observers:
                obs.on_vote(post, user, net)

    def accept_answer(self, user: User, answer: Answer):
        answer.question.accept_answer(answer, user)
        for obs in self.observers:
            obs.on_accept(answer, user)

    def search(self, query: str) -> list[Question]:
        return self.search_strategy.search(query, list(self.questions.values()))


# ─── Demo ────────────────────────────────────────────────────────────
def main():
    service = QAService()
    rep_mgr = ReputationManager()
    service.add_observer(rep_mgr)

    # Register users
    alice = service.register_user("alice", "alice@example.com")
    bob = service.register_user("bob", "bob@example.com")
    charlie = service.register_user("charlie", "charlie@example.com")

    print("=" * 60)
    print("1. POST QUESTION & ANSWERS")
    print("=" * 60)
    q1 = service.post_question(
        alice,
        "How to implement a LRU Cache in Python?",
        "I need an efficient O(1) LRU cache implementation...",
        ["python", "cache", "data-structures"])
    print(f"  {q1}")

    a1 = service.post_answer(bob, q1,
        "Use OrderedDict from collections. Move to end on access...")
    a2 = service.post_answer(charlie, q1,
        "Implement with a doubly-linked list + hashmap for O(1)...")
    print(f"  {a1}")
    print(f"  {a2}")

    # More questions for search
    q2 = service.post_question(alice, "Python decorator patterns",
                                "Best practices for decorators...",
                                ["python", "design-patterns"])
    q3 = service.post_question(bob, "Java vs Python for interviews",
                                "Which language should I choose?",
                                ["python", "java", "interview"])

    # ── Voting ──
    print(f"\n{'=' * 60}")
    print("2. VOTING & REPUTATION")
    print(f"{'=' * 60}")
    print(f"  Before voting: {bob}")
    service.vote(alice, a1, is_upvote=True)   # Alice upvotes Bob's answer
    service.vote(charlie, a1, is_upvote=True) # Charlie upvotes Bob's answer
    service.vote(alice, a2, is_upvote=True)   # Alice upvotes Charlie's answer
    print(f"  After upvotes: {bob}")
    print(f"  {a1}")
    print(f"  {a2}")

    # Downvote
    service.vote(charlie, q3, is_upvote=False)  # Charlie downvotes Bob's question
    print(f"  After downvote: {bob}")
    print(f"  Charlie (downvoter): {charlie}")

    # ── Accept Answer ──
    print(f"\n{'=' * 60}")
    print("3. ACCEPT ANSWER")
    print(f"{'=' * 60}")
    print(f"  Bob's rep before accept: {bob.reputation}")
    service.accept_answer(alice, a1)
    print(f"  Bob's rep after accept: {bob.reputation}")
    print(f"  Alice's rep (asker bonus): {alice.reputation}")
    print(f"  {a1}")

    # ── Comments ──
    print(f"\n{'=' * 60}")
    print("4. COMMENTS")
    print(f"{'=' * 60}")
    q1.add_comment(Comment(charlie, "Great question! I had this in an interview"))
    a1.add_comment(Comment(alice, "Thanks! The OrderedDict approach is clean"))
    for c in q1.comments:
        print(f"  {c}")
    for c in a1.comments:
        print(f"  {c}")

    # ── Search ──
    print(f"\n{'=' * 60}")
    print("5. SEARCH")
    print(f"{'=' * 60}")
    results = service.search("python")
    print(f"  Search 'python' ({len(results)} results):")
    for q in results:
        print(f"    {q}")

    service.search_strategy = MostVotedSearch()
    results = service.search("python")
    print(f"\n  Most Voted search 'python' ({len(results)} results):")
    for q in results:
        print(f"    {q}")

    # ── Question State ──
    print(f"\n{'=' * 60}")
    print("6. QUESTION STATE (Close/Reopen)")
    print(f"{'=' * 60}")
    print(f"  Status: {q3.state.get_name()}")
    q3.close("Off-topic")
    print(f"  After close: {q3.state.get_name()}")

    try:
        service.post_answer(charlie, q3, "Answering closed question...")
    except ValueError as e:
        print(f"  Cannot answer: {e}")

    q3.reopen()
    print(f"  After reopen: {q3.state.get_name()}")

    # ── Edge Cases ──
    print(f"\n{'=' * 60}")
    print("7. EDGE CASES")
    print(f"{'=' * 60}")

    # Self-voting
    try:
        service.vote(alice, q1, is_upvote=True)
    except ValueError as e:
        print(f"  Self-vote: {e}")

    # Non-author accepting
    try:
        service.accept_answer(bob, a2)
    except ValueError as e:
        print(f"  Wrong acceptor: {e}")

    # ── Summary ──
    print(f"\n{'=' * 60}")
    print("FINAL STATE")
    print(f"{'=' * 60}")
    for user in [alice, bob, charlie]:
        badges = ", ".join(str(b) for b in user.badges) if user.badges else "None"
        print(f"  {user} | Badges: {badges}")


if __name__ == "__main__":
    main()
