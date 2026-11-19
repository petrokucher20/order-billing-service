billing.py – початковий код (містить Common, Control та Stamp Coupling)
# Дефект 1 (Common Coupling): глобальна змінна змінюється та читається напряму


class CustomerProfile:
    def __init__(self, user_id, email, password_hash, city, loyalty_points):
        self.user_id = user_id
        self.email = email
        self.password_hash = password_hash
        self.city = city
        self.loyalty_points = loyalty_points

def calculate_delivery_cost(city: str, weight_kg: float) -> float:
    base_rate = 80.0 if city == "Kyiv" else (50.0 if city == "Ivano-Frankivsk" else 110.0)
    return base_rate + (weight_kg * 12.0)

# Дефект 3 (Control Coupling): параметр mode_flag керує внутрішнім розгалуженням функції
def process_standard_invoice(amount: float, city: str, weight_kg: float,
                             tax_rate: float = 0.20) -> dict:
    delivery = calculate_delivery_cost(city, weight_kg)
    total = (amount * (1 + tax_rate)) + delivery
    return {"status": "PROCESSED", "total": round(total, 2)}


def process_tax_exempt_invoice(amount: float, city: str, weight_kg: float) -> dict:
    # Податок не застосовується, глобальний стан не змінюється
    total = amount + calculate_delivery_cost(city, weight_kg)
    return {"status": "TAX_EXEMPT", "total": round(total, 2)}


# Колишня гілка else (CANCELLED) — також окрема функція, щоб зберегти поведінку
def process_cancelled_invoice() -> dict:
    return {"status": "CANCELLED", "total": 0.0}


if __name__ == "__main__":
    customer = CustomerProfile(1, "a@b.com", "hash", "Ivano-Frankivsk", 100)
    print(process_standard_invoice(1000, customer.city, 2))    # 1000*1.2 + 74 = 1274.0
    print(process_tax_exempt_invoice(1000, customer.city, 2))  # 1000 + 74 = 1074.0
    print(process_cancelled_invoice())

