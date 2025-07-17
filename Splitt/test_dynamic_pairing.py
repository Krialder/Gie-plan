#!/usr/bin/env python3
"""
Test script to verify the dynamic pairing functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import data
import schedule
import random

def test_dynamic_pairing():
    """Test the dynamic pairing functionality"""
    print("Testing Dynamic Pairing System")
    print("="*50)
    
    # Load current data
    data.reload_current_data()
    
    print(f"People: {data.PEOPLE}")
    print(f"Current year: {data.get_current_year()}")
    print()
    
    # Test multiple selections to see variety
    print("Testing multiple selections to verify dynamic pairing:")
    selection_count = {person: len(data.watering_history[person]) for person in data.PEOPLE}
    
    for i in range(10):
        print(f"\nSelection {i+1}:")
        selected = schedule.select_people_weighted_mean(selection_count, current_week_in_year=30+i)
        ersatz = schedule.select_ersatz_people_weighted_mean(selection_count, excluded_persons=selected, current_week_in_year=30+i)
        
        print(f"  Main persons: {selected[0]} and {selected[1]}")
        print(f"  Ersatz persons: {ersatz[0]} and {ersatz[1]}")
        
        # Update selection count for next iteration
        for person in selected:
            selection_count[person] += 1
    
    print("\n" + "="*50)
    print("Test completed! Check above for pairing variety.")
    print("If you see different combinations (not always the same pairs), the dynamic pairing is working!")

if __name__ == "__main__":
    test_dynamic_pairing()
