#!/usr/bin/env python3
"""
Test the updated multi-tiered smart pairing logic
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import data
from schedule import select_with_smart_pairing
import json

def test_multi_tiered_pairing():
    """Test the multi-tiered pairing logic"""
    
    print("TESTING MULTI-TIERED SMART PAIRING LOGIC")
    print("=" * 50)
    
    # Create test scenarios
    test_scenarios = [
        {
            "name": "Scenario 1: New + Experienced + Learning",
            "data": {
                "Jan": {"waterings": 15, "experience_level": None},      # experienced
                "Jeff": {"waterings": 12, "experience_level": None},     # experienced  
                "Antonia": {"waterings": 8, "experience_level": None},   # learning
                "Melissa": {"waterings": 18, "experience_level": None},  # experienced
                "Rosa": {"waterings": 2, "experience_level": None},      # new
                "Alexander": {"waterings": 3, "experience_level": None}  # new
            },
            "expected": "New person (Rosa/Alexander) paired with experienced person (Jan/Jeff/Melissa)"
        },
        {
            "name": "Scenario 2: New + Learning (no experienced)",
            "data": {
                "Jan": {"waterings": 6, "experience_level": None},      # learning
                "Jeff": {"waterings": 7, "experience_level": None},     # learning
                "Antonia": {"waterings": 5, "experience_level": None},   # learning
                "Melissa": {"waterings": 8, "experience_level": None},   # learning
                "Rosa": {"waterings": 1, "experience_level": None},      # new
                "Alexander": {"waterings": 2, "experience_level": None}  # new
            },
            "expected": "New person (Rosa/Alexander) paired with learning person (Jan/Jeff/Antonia/Melissa)"
        },
        {
            "name": "Scenario 3: Only Learning + Experienced (no new)",
            "data": {
                "Jan": {"waterings": 15, "experience_level": None},      # experienced
                "Jeff": {"waterings": 12, "experience_level": None},     # experienced  
                "Antonia": {"waterings": 8, "experience_level": None},   # learning
                "Melissa": {"waterings": 6, "experience_level": None},   # learning
                "Thomas": {"waterings": 14, "experience_level": None},   # experienced
                "Sarah": {"waterings": 7, "experience_level": None},     # learning
            },
            "expected": "Pure weight-based selection (highest scores)"
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n{scenario['name']}")
        print("-" * 60)
        
        # Setup test data
        with open('people_2027.json', 'w') as f:
            json.dump(scenario['data'], f, indent=2)
        
        # Reload data
        data.reload_current_data()
        
        # Manually set up watering history based on the waterings count
        data.watering_history = {}
        for person in data.PEOPLE:
            if person in scenario['data']:
                waterings_count = scenario['data'][person]['waterings']
                # Create fake watering history entries
                data.watering_history[person] = []
                for i in range(waterings_count):
                    data.watering_history[person].append(f"2027 KW {i+1}: {person} and someone")
            else:
                # If person not in scenario data, give them 0 waterings
                data.watering_history[person] = []
        
        # Show current state
        print(f"People: {data.PEOPLE}")
        print("\nExperience levels and watering counts:")
        for person in data.PEOPLE:
            count = len(data.watering_history.get(person, []))
            level = data.get_person_experience_level(person)
            print(f"  {person:<12} | Count: {count:2d} | Level: {level}")
        
        # Get experience groups
        new_people = data.get_new_people()
        experienced_people = data.get_experienced_people()
        
        print(f"\nNew people: {new_people}")
        print(f"Experienced people: {experienced_people}")
        
        # Test selection multiple times
        print(f"\nExpected: {scenario['expected']}")
        print("Selection results:")
        
        selection_count = {person: len(data.watering_history.get(person, [])) for person in data.PEOPLE}
        
        for i in range(5):
            selected = select_with_smart_pairing(selection_count, 20, new_people, experienced_people)
            
            # Analyze the selection
            if len(selected) == 2:
                person1, person2 = selected
                level1 = data.get_person_experience_level(person1)
                level2 = data.get_person_experience_level(person2)
                count1 = len(data.watering_history.get(person1, []))
                count2 = len(data.watering_history.get(person2, []))
                
                print(f"  Selection {i+1}: {person1} ({level1}, {count1}) + {person2} ({level2}, {count2})")
            else:
                print(f"  Selection {i+1}: {selected}")
            
            # Update selection count for next iteration
            for person in selected:
                selection_count[person] += 1
        
        print(f"\n✅ Scenario completed")
    
    print("\n" + "="*50)
    print("✅ Multi-tiered pairing logic test completed")
    print("Key improvements:")
    print("  - Priority 1: New + Experienced pairing")
    print("  - Priority 2: New + Learning pairing (when no experienced)")
    print("  - Priority 3: Weight-based selection (when no new people)")
    print("  - Learning people always considered in selection pool")
    print("  - Weight remains the primary factor for fairness")
    
    # Restore original data
    original_data = {
        "Jan": {"waterings": 9, "experience_level": None},
        "Jeff": {"waterings": 9, "experience_level": None},
        "Antonia": {"waterings": 6, "experience_level": None},
        "Melissa": {"waterings": 10, "experience_level": None},
        "Rosa": {"waterings": 6, "experience_level": None},
        "Alexander": {"waterings": 6, "experience_level": None}
    }
    
    with open('people_2027.json', 'w') as f:
        json.dump(original_data, f, indent=2)
    
    print("\n✅ Original data restored")

if __name__ == "__main__":
    test_multi_tiered_pairing()
