def vacuum_agent(location, status):
    if status == "Dirty":
        return "Suck"
    elif location == "A":
        return "Move Right"
    else:
        return "Move Left"


rooms = {
    "A": "Dirty",
    "B": "Dirty"
}

location = "A"

print("=" * 45)
print("       VACUUM CLEANER - SIMPLE REFLEX AGENT")
print("=" * 45)

print("\nInitial Environment")
print(f"  Room A : {rooms['A']}")
print(f"  Room B : {rooms['B']}")
print(f"  Vacuum : Room {location}")

print("\n" + "-" * 45)

while rooms["A"] == "Dirty" or rooms["B"] == "Dirty":

    status = rooms[location]
    action = vacuum_agent(location, status)

    print(f"📍 Current Location : Room {location}")
    print(f"🧹 Room Status      : {status}")
    print(f"⚡ Agent Action      : {action}")

    if action == "Suck":
        rooms[location] = "Clean"
    elif action == "Move Right":
        location = "B"
    elif action == "Move Left":
        location = "A"

    print("-" * 45)

print("\n" + "=" * 45)
print("             CLEANING COMPLETED")
print("=" * 45)
print(f"  Room A : {rooms['A']} ✅")
print(f"  Room B : {rooms['B']} ✅")
print("  Vacuum Cleaner : All rooms are clean! 🧹")
print("=" * 45)
