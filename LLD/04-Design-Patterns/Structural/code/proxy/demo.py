"""Demo: Proxy pattern - lazy loading and access control."""

from proxy import LazyImageProxy
from protection_proxy import AdminOnlyProxy


def main():
    print("=" * 50)
    print("PROXY PATTERN")
    print("=" * 50)

    # Virtual proxy - lazy loading
    print("\n--- Lazy Image Proxy ---")
    img = LazyImageProxy("sunset.jpg")
    print(f"  Proxy created (image NOT loaded yet)")
    print(f"  Filename: {img.get_filename()}")
    print(f"  First display:")
    print(f"  {img.display()}")
    print(f"  Second display (cached):")
    print(f"  {img.display()}")

    # Protection proxy
    print("\n--- Protection Proxy (admin) ---")
    admin_img = AdminOnlyProxy("secret.jpg", "admin")
    print(f"  {admin_img.display()}")

    print("\n--- Protection Proxy (viewer) ---")
    viewer_img = AdminOnlyProxy("secret.jpg", "viewer")
    print(f"  {viewer_img.display()}")


if __name__ == "__main__":
    main()
