"""
Social Media Platform (Twitter-like) - Low Level Design Implementation

Design Patterns Used:
- Observer Pattern: Follow/notification system
- Strategy Pattern: Feed generation (Chronological, Engagement-based)
- Command Pattern: Post actions (like, comment) with undo
- Factory Pattern: Content creation
- Iterator Pattern: Feed pagination
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional
from collections import defaultdict
import re
import uuid


# ============================================================
# Command Pattern: Post Actions with Undo
# ============================================================

class PostAction(ABC):
    @abstractmethod
    def execute(self) -> str:
        pass
    @abstractmethod
    def undo(self) -> str:
        pass


class LikeAction(PostAction):
    def __init__(self, user: "User", post: "Post"):
        self.user = user
        self.post = post

    def execute(self) -> str:
        if self.user in self.post.likes:
            return f"{self.user.username} already likes this post."
        self.post.likes.add(self.user)
        return f"{self.user.username} liked post by {self.post.author.username}"

    def undo(self) -> str:
        if self.user not in self.post.likes:
            return f"{self.user.username} hasn't liked this post."
        self.post.likes.discard(self.user)
        return f"{self.user.username} unliked post by {self.post.author.username}"


class CommentAction(PostAction):
    def __init__(self, user: "User", post: "Post", content: str):
        self.user = user
        self.post = post
        self.content = content
        self.comment: Optional["Comment"] = None

    def execute(self) -> str:
        self.comment = Comment(self.user, self.post, self.content)
        self.post.comments.append(self.comment)
        return (f"{self.user.username} commented on {self.post.author.username}'s post: "
                f'"{self.content}"')

    def undo(self) -> str:
        if self.comment and self.comment in self.post.comments:
            self.post.comments.remove(self.comment)
            return f"{self.user.username} deleted their comment."
        return "Comment not found."


# ============================================================
# Observer Pattern: Notification System
# ============================================================

class NotificationObserver(ABC):
    @abstractmethod
    def notify(self, event: str, data: dict):
        pass


class ConsoleNotifier(NotificationObserver):
    def notify(self, event: str, data: dict):
        if event == "new_post":
            print(f"  [NOTIFY] {data['follower']}: "
                  f"{data['author']} posted: \"{data['preview']}\"")
        elif event == "new_follower":
            print(f"  [NOTIFY] {data['followed']}: "
                  f"{data['follower']} started following you!")
        elif event == "new_like":
            print(f"  [NOTIFY] {data['author']}: "
                  f"{data['liker']} liked your post.")
        elif event == "new_message":
            print(f"  [NOTIFY] {data['receiver']}: "
                  f"New DM from {data['sender']}")


# ============================================================
# Strategy Pattern: Feed Generation
# ============================================================

class FeedStrategy(ABC):
    @abstractmethod
    def generate_feed(self, user: "User", all_posts: List["Post"]) -> List["Post"]:
        pass


class ChronologicalFeed(FeedStrategy):
    """Sort posts by timestamp, newest first."""
    def generate_feed(self, user, all_posts):
        following_ids = {u.user_id for u in user.following}
        blocked_ids = {u.user_id for u in user.blocked_users}
        feed = [p for p in all_posts
                if p.author.user_id in following_ids
                and p.author.user_id not in blocked_ids]
        feed.sort(key=lambda p: p.timestamp, reverse=True)
        return feed


class EngagementFeed(FeedStrategy):
    """Score posts by engagement: likes + comments*2 + recency bonus."""
    def generate_feed(self, user, all_posts):
        following_ids = {u.user_id for u in user.following}
        blocked_ids = {u.user_id for u in user.blocked_users}
        feed = [p for p in all_posts
                if p.author.user_id in following_ids
                and p.author.user_id not in blocked_ids]

        now = datetime.now()
        def score(post):
            hours_old = (now - post.timestamp).total_seconds() / 3600
            recency_bonus = max(0, 100 - hours_old * 2)
            return len(post.likes) * 1.0 + len(post.comments) * 2.0 + recency_bonus

        feed.sort(key=score, reverse=True)
        return feed


# ============================================================
# Iterator Pattern: Feed Pagination
# ============================================================

class FeedIterator:
    def __init__(self, items: List["Post"], page_size: int = 5):
        self.items = items
        self.page_size = page_size
        self.position = 0

    def has_next(self) -> bool:
        return self.position < len(self.items)

    def next_page(self) -> List["Post"]:
        page = self.items[self.position:self.position + self.page_size]
        self.position += self.page_size
        return page

    def total_items(self) -> int:
        return len(self.items)


# ============================================================
# Core Models
# ============================================================

class Comment:
    def __init__(self, author: "User", post: "Post", content: str):
        self.comment_id = str(uuid.uuid4())[:8]
        self.author = author
        self.post = post
        self.content = content
        self.timestamp = datetime.now()

    def __str__(self):
        return f"  @{self.author.username}: {self.content}"


class Post:
    def __init__(self, author: "User", content: str,
                 timestamp: Optional[datetime] = None):
        self.post_id = str(uuid.uuid4())[:8]
        self.author = author
        self.content = content
        self.hashtags = self._extract_hashtags(content)
        self.timestamp = timestamp or datetime.now()
        self.likes: Set["User"] = set()
        self.comments: List[Comment] = []

    @staticmethod
    def _extract_hashtags(content: str) -> List[str]:
        return list(set(tag.lower() for tag in re.findall(r"#(\w+)", content)))

    def get_engagement_score(self) -> float:
        hours_old = (datetime.now() - self.timestamp).total_seconds() / 3600
        recency = max(0, 100 - hours_old * 2)
        return len(self.likes) + len(self.comments) * 2 + recency

    def __str__(self):
        tags = " ".join(f"#{t}" for t in self.hashtags) if self.hashtags else ""
        return (f"[@{self.author.username} | {self.timestamp.strftime('%H:%M')}] "
                f"{self.content}\n"
                f"    Likes: {len(self.likes)} | Comments: {len(self.comments)}"
                f"{' | Tags: ' + tags if tags else ''}")


class DirectMessage:
    def __init__(self, sender: "User", receiver: "User", content: str):
        self.message_id = str(uuid.uuid4())[:8]
        self.sender = sender
        self.receiver = receiver
        self.content = content
        self.timestamp = datetime.now()
        self.read = False

    def __str__(self):
        status = "read" if self.read else "unread"
        return f"[{self.timestamp.strftime('%H:%M')}] @{self.sender.username}: {self.content} ({status})"


class User:
    def __init__(self, username: str, email: str, bio: str = ""):
        self.user_id = str(uuid.uuid4())[:8]
        self.username = username
        self.email = email
        self.bio = bio
        self.followers: Set["User"] = set()
        self.following: Set["User"] = set()
        self.posts: List[Post] = []
        self.blocked_users: Set["User"] = set()
        self.messages: List[DirectMessage] = []
        self._observers: List[NotificationObserver] = []

    def add_observer(self, observer: NotificationObserver):
        self._observers.append(observer)

    def _notify_all(self, event: str, data: dict):
        for obs in self._observers:
            obs.notify(event, data)

    def follow(self, other: "User") -> str:
        if other == self:
            return "Cannot follow yourself."
        if other in self.blocked_users:
            return f"Cannot follow blocked user @{other.username}."
        if other in self.following:
            return f"Already following @{other.username}."
        self.following.add(other)
        other.followers.add(self)
        other._notify_all("new_follower", {
            "follower": self.username, "followed": other.username
        })
        return f"@{self.username} now follows @{other.username}"

    def unfollow(self, other: "User") -> str:
        if other not in self.following:
            return f"Not following @{other.username}."
        self.following.discard(other)
        other.followers.discard(self)
        return f"@{self.username} unfollowed @{other.username}"

    def block(self, other: "User") -> str:
        self.blocked_users.add(other)
        self.following.discard(other)
        other.followers.discard(self)
        other.following.discard(self)
        self.followers.discard(other)
        return f"@{self.username} blocked @{other.username}"

    def __hash__(self):
        return hash(self.user_id)

    def __eq__(self, other):
        return isinstance(other, User) and self.user_id == other.user_id

    def __str__(self):
        return (f"@{self.username} | Followers: {len(self.followers)} | "
                f"Following: {len(self.following)} | Posts: {len(self.posts)}")


# ============================================================
# Platform
# ============================================================

class SocialMediaPlatform:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.posts: List[Post] = []
        self.hashtag_index: Dict[str, List[Post]] = defaultdict(list)
        self._notifier = ConsoleNotifier()

    def register_user(self, username: str, email: str, bio: str = "") -> User:
        if username in self.users:
            raise ValueError(f"Username @{username} already taken.")
        user = User(username, email, bio)
        user.add_observer(self._notifier)
        self.users[username] = user
        return user

    def create_post(self, user: User, content: str,
                    timestamp: Optional[datetime] = None) -> Post:
        post = Post(user, content, timestamp)
        user.posts.append(post)
        self.posts.append(post)

        # Index hashtags
        for tag in post.hashtags:
            self.hashtag_index[tag].append(post)

        # Notify followers
        for follower in user.followers:
            if user not in follower.blocked_users:
                follower._notify_all("new_post", {
                    "follower": follower.username,
                    "author": user.username,
                    "preview": content[:50]
                })
        return post

    def like_post(self, user: User, post: Post) -> str:
        action = LikeAction(user, post)
        result = action.execute()
        if "liked" in result:
            post.author._notify_all("new_like", {
                "author": post.author.username,
                "liker": user.username
            })
        return result

    def unlike_post(self, user: User, post: Post) -> str:
        action = LikeAction(user, post)
        return action.undo()

    def comment_on_post(self, user: User, post: Post, content: str) -> str:
        action = CommentAction(user, post, content)
        return action.execute()

    def get_feed(self, user: User,
                 strategy: Optional[FeedStrategy] = None) -> FeedIterator:
        strat = strategy or ChronologicalFeed()
        feed_posts = strat.generate_feed(user, self.posts)
        return FeedIterator(feed_posts)

    def search_posts(self, query: str) -> List[Post]:
        query_lower = query.lower()
        return [p for p in self.posts if query_lower in p.content.lower()]

    def search_by_hashtag(self, tag: str) -> List[Post]:
        return self.hashtag_index.get(tag.lower().lstrip("#"), [])

    def get_trending(self, top_n: int = 5) -> List[tuple]:
        tag_counts = [(tag, len(posts)) for tag, posts in self.hashtag_index.items()]
        tag_counts.sort(key=lambda x: x[1], reverse=True)
        return tag_counts[:top_n]

    def send_message(self, sender: User, receiver: User, content: str) -> str:
        if sender in receiver.blocked_users:
            return "Cannot send message to this user."
        msg = DirectMessage(sender, receiver, content)
        sender.messages.append(msg)
        receiver.messages.append(msg)
        receiver._notify_all("new_message", {
            "sender": sender.username, "receiver": receiver.username
        })
        return f"Message sent to @{receiver.username}"


# ============================================================
# Demo
# ============================================================

def main():
    print("=" * 65)
    print("     SOCIAL MEDIA PLATFORM - LOW LEVEL DESIGN DEMO")
    print("=" * 65)

    platform = SocialMediaPlatform()

    # ---- Register Users ----
    print("\n--- User Registration ---")
    alice = platform.register_user("alice", "alice@mail.com", "Software Engineer")
    bob = platform.register_user("bob", "bob@mail.com", "Data Scientist")
    charlie = platform.register_user("charlie", "charlie@mail.com", "Designer")
    diana = platform.register_user("diana", "diana@mail.com", "Product Manager")

    for u in [alice, bob, charlie, diana]:
        print(f"  Registered: {u}")

    # ---- Follow ----
    print("\n--- Follow Users ---")
    print(f"  {alice.follow(bob)}")
    print(f"  {alice.follow(charlie)}")
    print(f"  {bob.follow(alice)}")
    print(f"  {charlie.follow(alice)}")
    print(f"  {diana.follow(alice)}")
    print(f"  {diana.follow(bob)}")

    # ---- Create Posts (with simulated timestamps for variety) ----
    print("\n--- Create Posts ---")
    now = datetime.now()
    p1 = platform.create_post(alice, "Just started learning #LLD #SystemDesign!",
                               now - timedelta(hours=5))
    p2 = platform.create_post(bob, "Great article on #Python and #MachineLearning",
                               now - timedelta(hours=3))
    p3 = platform.create_post(charlie, "New UI design ready! #Design #UX",
                               now - timedelta(hours=2))
    p4 = platform.create_post(alice, "Design patterns are amazing! #LLD #DesignPatterns",
                               now - timedelta(hours=1))
    p5 = platform.create_post(bob, "Working on a cool #Python project #Coding",
                               now - timedelta(minutes=30))

    for p in [p1, p2, p3, p4, p5]:
        print(f"\n  {p}")

    # ---- Like and Comment ----
    print("\n--- Like and Comment ---")
    print(f"  {platform.like_post(bob, p1)}")
    print(f"  {platform.like_post(charlie, p1)}")
    print(f"  {platform.like_post(diana, p1)}")
    print(f"  {platform.like_post(alice, p2)}")
    print(f"  {platform.like_post(diana, p4)}")

    print(f"  {platform.comment_on_post(bob, p1, 'Great start! Keep going!')}")
    print(f"  {platform.comment_on_post(charlie, p1, 'LLD is so important!')}")
    print(f"  {platform.comment_on_post(alice, p2, 'Thanks for sharing!')}")

    # ---- Feed: Chronological ----
    print("\n--- Alice's Feed (Chronological) ---")
    feed_iter = platform.get_feed(alice, ChronologicalFeed())
    page = feed_iter.next_page()
    for i, post in enumerate(page, 1):
        print(f"  {i}. {post}")

    # ---- Feed: Engagement-based ----
    print("\n--- Diana's Feed (Engagement-Based) ---")
    feed_iter = platform.get_feed(diana, EngagementFeed())
    page = feed_iter.next_page()
    for i, post in enumerate(page, 1):
        print(f"  {i}. {post}")
        print(f"       Engagement Score: {post.get_engagement_score():.1f}")

    # ---- Search ----
    print("\n--- Search Posts for 'Python' ---")
    results = platform.search_posts("Python")
    for p in results:
        print(f"  {p}")

    # ---- Hashtag Search ----
    print("\n--- Search by Hashtag: #LLD ---")
    results = platform.search_by_hashtag("lld")
    for p in results:
        print(f"  {p}")

    # ---- Trending ----
    print("\n--- Trending Hashtags ---")
    trending = platform.get_trending(5)
    for i, (tag, count) in enumerate(trending, 1):
        print(f"  {i}. #{tag} ({count} posts)")

    # ---- Direct Message ----
    print("\n--- Direct Messages ---")
    print(f"  {platform.send_message(alice, bob, 'Hey Bob, loved your Python article!')}")
    print(f"  {platform.send_message(bob, alice, 'Thanks Alice! Let us collaborate.')}")

    # ---- Unlike (Undo) ----
    print("\n--- Unlike (Command Undo) ---")
    print(f"  {platform.unlike_post(diana, p1)}")
    print(f"  Post p1 likes after unlike: {len(p1.likes)}")

    # ---- Block User ----
    print("\n--- Block User ---")
    print(f"  {alice.block(charlie)}")
    print(f"\n  Alice's feed after blocking Charlie (Chronological):")
    feed_iter = platform.get_feed(alice, ChronologicalFeed())
    page = feed_iter.next_page()
    for i, post in enumerate(page, 1):
        print(f"    {i}. {post}")
    print(f"  (Charlie's posts filtered out)")

    # ---- Final Stats ----
    print("\n--- Final User Stats ---")
    for u in [alice, bob, charlie, diana]:
        print(f"  {u}")


if __name__ == "__main__":
    main()
