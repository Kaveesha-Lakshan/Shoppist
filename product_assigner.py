# product_assigner.py

def assign_products_to_racks(rack_ids):
    """
    Prompts user to assign a product to each rack.
    Returns a dictionary: { rack_id: product_name }
    """
    product_map = {}
    print("\n🛒 Assign products to each rack:")
    for rack in rack_ids:
        product = input(f"{rack} → Product: ").strip()
        product_map[rack] = product if product else "unassigned"
    return product_map
