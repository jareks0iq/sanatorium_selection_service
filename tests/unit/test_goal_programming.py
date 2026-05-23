from pytest import approx

from domain.goal_programming import recommend
from domain.model import Sanatorium, Tag, UserProfile


def make_profile(
    budget=50000,
    region="Краснодарский край",
    tags=None,
    budget_weight=0,
    region_weight=0,
    medical_weight=0,
    services_weight=0,
    conditions_weight=0,
):
    return UserProfile(
        id=1,
        user_id=1,
        goal="лечение",
        budget=budget,
        region=region,
        tags=tags if tags is not None else [],
        budget_weight=budget_weight,
        region_weight=region_weight,
        medical_weight=medical_weight,
        services_weight=services_weight,
        conditions_weight=conditions_weight,
    )


def make_sanatorium(
    id=1,
    name="Тестовый санаторий",
    budget=50000,
    region="Краснодарский край",
    tags=None,
    food="трёхразовое",
    rating=4.5,
):
    return Sanatorium(
        id=id,
        name=name,
        budget=budget,
        region=region,
        tags=tags if tags is not None else [],
        food=food,
        rating=rating,
    )


def make_tag(id, category, name="тег"):
    return Tag(id=id, name=name, category=category)


def test_cheaper_sanatorium_has_zero_budget_deviation():
    profile = make_profile(
        budget=50000,
        budget_weight=1,
    )
    sanatorium = make_sanatorium(budget=40000)
    results = recommend([sanatorium], profile)
    score, returned = results[0]
    assert score == 0


def test_expensive_sanatorium_has_budget_deviation():
    profile = make_profile(
        budget=50000,
        budget_weight=1,
    )
    sanatorium = make_sanatorium(budget=60000)
    results = recommend([sanatorium], profile)
    score, returned = results[0]
    assert score > 0


def test_sanatorium_with_same_region_has_zero_deviation():
    profile = make_profile(region_weight=1)
    sanatorium = make_sanatorium(region=profile.region)
    results = recommend([sanatorium], profile)
    score, returned = results[0]
    assert score == 0


def test_sanatorium_with_another_region_has_deviation():
    profile = make_profile(region_weight=1)
    sanatorium = make_sanatorium(region="Крым")
    results = recommend([sanatorium], profile)
    score, returned = results[0]
    assert score > 0


def test_full_tag_match_has_zero_deviation():
    test_tags = [make_tag(1, "medical"), make_tag(2, "medical")]
    profile = make_profile(medical_weight=1, tags=test_tags)
    sanatorium = make_sanatorium(tags=test_tags)
    results = recommend([sanatorium], profile)
    score, returned = results[0]
    assert score == 0


def test_partly_tag_match_has_proportional_deviation():
    test_tags = [make_tag(1, "medical"), make_tag(2, "medical")]
    profile = make_profile(medical_weight=1, tags=test_tags)
    sanatorium = make_sanatorium(tags=[make_tag(2, "medical")])
    results = recommend([sanatorium], profile)
    score, returned = results[0]
    assert score == approx(0.5)


def test_no_tag_match_has_deviation():
    test_tags = [make_tag(1, "medical"), make_tag(2, "medical")]
    profile = make_profile(medical_weight=1, tags=test_tags)
    sanatorium = make_sanatorium(tags=[make_tag(3, "medical")])
    results = recommend([sanatorium], profile)
    score, returned = results[0]
    assert score == 1


def test_no_user_tags_in_category_means_zero_deviation():
    test_tags = [make_tag(1, "medical"), make_tag(2, "medical")]
    profile = make_profile(
        medical_weight=1,
    )
    sanatorium = make_sanatorium(tags=test_tags)
    results = recommend([sanatorium], profile)
    score, returned = results[0]
    assert score == 0


def test_sanatoriums_sorted_by_score_ascending():
    profile = make_profile(
        budget=50000, budget_weight=1, region_weight=1, region="Красндораский край"
    )
    best = make_sanatorium(id=1, budget=40000, region=profile.region)
    middle = make_sanatorium(id=2, budget=60000, region=profile.region)
    worst = make_sanatorium(id=3, budget=60000, region="Крым")

    results = recommend([worst, middle, best], profile)
    ordered_ids = [sanat.id for score, sanat in results]
    assert ordered_ids == [1, 2, 3]
