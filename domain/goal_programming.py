def recommend(sanatoriums: list, profile):
    scored = []
    sum_weights = profile.budget_weight + profile.region_weight + profile.medical_weight + profile.services_weight + profile.conditions_weight
    w_budget = profile.budget_weight / sum_weights
    w_region = profile.region_weight / sum_weights
    w_medical = profile.medical_weight / sum_weights
    w_services = profile.services_weight / sum_weights
    w_conditions = profile.conditions_weight / sum_weights
    profile_medical = {t.id for t in profile.tags if t.category == "medical"}
    profile_services = {t.id for t in profile.tags if t.category == "services"}
    profile_conditions = {t.id for t in profile.tags if t.category == "conditions"}
    for s in sanatoriums:
        budget_norm = max(0, s.budget - profile.budget) / profile.budget
        budget = budget_norm * w_budget

        region_norm = 0 if profile.region == s.region else 1
        region = region_norm * w_region

        sanat_medical = {t.id for t in s.tags if t.category == "medical"}
        sanat_services = {t.id for t in s.tags if t.category == "services"}
        sanat_conditions = {t.id for t in s.tags if t.category == "conditions"}

        medical_good = len(profile_medical & sanat_medical)
        services_good = len(profile_services & sanat_services)
        conditions_good = len(profile_conditions & sanat_conditions)
        medical = (1 - medical_good / len(profile_medical)) * w_medical if len(profile_medical) > 0 else 0
        services = (1 - services_good / len(profile_services)) * w_services if len(profile_services) > 0 else 0
        conditions = (1 - conditions_good / len(profile_conditions)) * w_conditions if len(profile_conditions) > 0 else 0

        score = budget + region + medical + services + conditions
        scored.append((score, s))

    scored.sort(key=lambda x: x[0])
    return scored
