from datetime import timezone

from promotion.models import Coupon, Promotion


def apply_promotions_to_cart(cart):
    """
    Apply the best promotion to the cart.
    :param cart: A dictionary representing the cart, containing product and price information.
    :return: A tuple containing the total discount and the updated cart with discounts applied.
    """
    total_discount = 0
    now = timezone.now()

    # Loop through cart items
    for item in cart['items']:
        product = item['product']
        applicable_promotions = product.promotions.filter(
            start_date__lte=now, 
            end_date__gte=now, 
            is_active=True
        )

        # Apply the highest promotion available to the product
        best_promotion = None
        best_discount_value = 0
        for promotion in applicable_promotions:
            if promotion.discount_type == Promotion.PERCENTAGE:
                discount_value = item['price'] * (promotion.discount_value / 100)
            elif promotion.discount_type == Promotion.FIXED:
                discount_value = promotion.discount_value
            elif promotion.discount_type == Promotion.FREE_SHIPPING:
                discount_value = item['shipping_cost']

            # Track the best discount
            if discount_value > best_discount_value:
                best_promotion = promotion
                best_discount_value = discount_value

        if best_promotion:
            total_discount += best_discount_value
            item['discount'] = best_discount_value  # Apply discount to the item

    cart['total_discount'] = total_discount
    cart['total_price_after_discount'] = cart['total_price'] - total_discount

    return total_discount, cart


def validate_and_apply_coupon(cart, coupon_code, user=None):
    """
    Validate the given coupon code for the user and apply the coupon discount to the cart if valid.
    :param cart: A dictionary representing the cart, containing product and price information.
    :param coupon_code: The coupon code entered by the user.
    :param user: The current user applying the coupon.
    :return: A tuple containing the coupon discount and the updated cart.
    """
    try:
        coupon = Coupon.objects.get(code=coupon_code)
    except Coupon.DoesNotExist:
        raise ValueError("Invalid coupon code.")

    if not coupon.is_valid(user=user):
        raise ValueError("This coupon is either expired, inactive, or has reached its usage limit.")

    # Check the associated promotion for the coupon
    promotion = coupon.promotion
    if not promotion.is_valid():
        raise ValueError("The promotion associated with this coupon is no longer valid.")

    coupon_discount = 0
    if promotion.discount_type == Promotion.PERCENTAGE:
        coupon_discount = cart['total_price'] * (promotion.discount_value / 100)
    elif promotion.discount_type == Promotion.FIXED:
        coupon_discount = promotion.discount_value
    elif promotion.discount_type == Promotion.FREE_SHIPPING:
        coupon_discount = cart['shipping_cost']

    # Apply the coupon discount
    cart['coupon_discount'] = coupon_discount
    cart['total_price_after_coupon'] = cart['total_price_after_discount'] - coupon_discount
    coupon.times_used += 1  # Increment usage count
    coupon.save()

    return coupon_discount, cart
