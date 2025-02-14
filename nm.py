import subprocess


def run_command(command):
    """Berilgan Django buyruqni ishga tushirish."""
    try:
        subprocess.run(f"python manage.py {command}", shell=True, check=True)
    except KeyboardInterrupt:
        print("\n❌ Buyruq to‘xtatildi!")
    except Exception as e:
        print(f"\n❌ Xato: {e}")


def main():
    """Foydalanuvchiga tanlash uchun Django buyruqlarini chiqarish."""
    commands = [
        "\n1️⃣ runserver  - Serverni ishga tushirish",
        "\n2️⃣ makemigrations  - Model o‘zgarishlarini yaratish",
        "\n3️⃣ migrate  - O‘zgarishlarni bazaga qo‘llash",
        "\n4️⃣ createsuperuser  - Admin user yaratish",
        "\n5️⃣ startapp  - Yangi app yaratish",
        "\n0️⃣ Chiqish",
    ]

    print("\n🔹 Django buyruqlari:")
    for cmd in commands:
        print(cmd)

    choice = input("\n📌 Buyruqni tanlang (raqam kiriting): ").strip()

    if choice == "1":
        run_command("runserver")
    elif choice == "2":
        run_command("makemigrations")
    elif choice == "3":
        run_command("migrate")
    elif choice == "4":
        run_command("createsuperuser")
    elif choice == "5":
        app_name = input("\n📌 Yangi app nomini kiriting: ").strip()
        if app_name:
            run_command(f"startapp {app_name}")
    elif choice == "0":
        print("\n✅ Dasturdan chiqildi!")
        return
    else:
        print("\n⚠️ Noto‘g‘ri tanlov! Iltimos, raqam kiriting.")


if __name__ == "__main__":
    main()
