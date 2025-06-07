import random
import time
import argparse

# --- Configuration ---
NUM_TOTAL_UNIQUE_ITEMS = 60000  # Total possible items an SE might encounter
NUM_HIGH_VALUE_ITEMS_IN_LIST = 30000 # N: Number of items considered "high-value"


ALL_POSSIBLE_ITEMS = [f"ITEM_{i:05d}" for i in range(NUM_TOTAL_UNIQUE_ITEMS)]

HIGH_VALUE_ITEMS_LIST = random.sample(ALL_POSSIBLE_ITEMS, NUM_HIGH_VALUE_ITEMS_IN_LIST)
N = len(HIGH_VALUE_ITEMS_LIST) # This is our N for complexity calculations

TIER_CONFIG = {
    "Junior": {"base_rate": 40, "hv_bonus_multiplier": 1.0},
    "Senior": {"base_rate": 50, "hv_bonus_multiplier": 1.2},
    "Principal": {"base_rate": 60, "hv_bonus_multiplier": 1.5},
}
BASE_HIGH_VALUE_ITEM_BONUS = 10 # Adjusted bonus for more frequent "hits"
ENGAGEMENT_BONUS_PER_UNIQUE_ITEM = 1 # Adjusted bonus
# --- End Configuration ---

def calculate_per_diem(trip_log, employee_tier):
    """
    Calculates per diem based on a trip log of items encountered and employee tier.
    trip_log: A list of (item_id, deal_potential_score) tuples.
    employee_tier: String ("Junior", "Senior", "Principal")
    This version uses a LIST for checking high-value items.
    """
    total_per_diem = 0
    tier_details = TIER_CONFIG.get(employee_tier)
    if not tier_details:
        raise ValueError(f"Invalid employee tier: {employee_tier}")

    base_daily_rate = tier_details["base_rate"] # This is now more like a base interaction rate
    hv_bonus_tier_multiplier = tier_details["hv_bonus_multiplier"]

    visited_items_for_engagement_bonus = set()

    for day_index, (item_encountered, deal_potential) in enumerate(trip_log):
        interaction_value = base_daily_rate 
        visited_items_for_engagement_bonus.add(item_encountered)

        if item_encountered in HIGH_VALUE_ITEMS_LIST: 
            tier_adjusted_hv_bonus = BASE_HIGH_VALUE_ITEM_BONUS * hv_bonus_tier_multiplier
            final_hv_bonus_for_interaction = tier_adjusted_hv_bonus * deal_potential
            interaction_value += final_hv_bonus_for_interaction
        
        total_per_diem += interaction_value

    # Add engagement bonus
    engagement_total_bonus = len(visited_items_for_engagement_bonus) * ENGAGEMENT_BONUS_PER_UNIQUE_ITEM
    total_per_diem += engagement_total_bonus
    
    return total_per_diem

def generate_trip_log_items(num_interactions, items_pool):
    """Generates a random trip log with (item_id, deal_potential) tuples."""
    trip = []
    for _ in range(num_interactions):
        item = random.choice(items_pool)
        deal_potential = round(random.uniform(1.0, 3.0), 1)
        trip.append((item, deal_potential))
    return trip

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate per diem for a sales engineer based on item interactions.")
    parser.add_argument(
        "--interactions",
        type=int, 
        default=500,
        help="Number of item interactions in the log (default: 500)"
    )
    parser.add_argument(
        "--tier", 
        type=str, 
        default="Principal", 
        choices=["Junior", "Senior", "Principal"],
        help="Employee tier (default: Principal)"
    )
    args = parser.parse_args()

    num_logged_interactions = args.interactions 
    selected_tier = args.tier
    
    print(f"\nConfiguration: {num_logged_interactions} logged interactions (M), Tier: {selected_tier}\n")


    trip_log = generate_trip_log_items(num_logged_interactions, ALL_POSSIBLE_ITEMS)

    print(f"\nCalculating per diem (Initial  Version)...")
    start_time = time.time()
    
    total_per_diem_calculated = calculate_per_diem(trip_log, selected_tier)
    
    end_time = time.time()
    time_taken_ms = (end_time - start_time) * 1000
    
    
    print(f"Total Per Diem (Initial  Version): Value ${total_per_diem_calculated:,.2f}\n") # Changed label
    print(f"Time taken (Initial  Version): {time_taken_ms:.2f} ms")
    if time_taken_ms > 1000:
        print(f"Which is roughly: {time_taken_ms/1000:.2f} seconds")
