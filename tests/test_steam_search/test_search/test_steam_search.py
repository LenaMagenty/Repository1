import pytest
from pages.home_page import HomePage


@pytest.mark.parametrize('game_name,n', [
    ('The Witcher', 10),
    ('Fallout', 20),
])
def test_search_sort_highest_price_and_get_n(driver, game_name, n):
    home = HomePage(driver).open_home()
    results = home.search(game_name)

    results.sort_by_highest_price()
    titles = results.get_first_n_titles(n)

    assert len(titles) == n, f'Ожидали {n} игр, получили {len(titles)}'

    for i, title in enumerate(titles, start=1):
        print(f'{i}. {title}')

