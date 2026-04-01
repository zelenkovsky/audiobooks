import pytest
from generate import extract_author, parse_line


class TestExtractAuthorDashPattern:
    """Pattern: Author - Title (first space-surrounded dash separates author)."""

    def test_asimov(self):
        assert (
            extract_author("Айзек Азимов - 'Я - робот' [Радиоспектакль]")
            == "Айзек Азимов"
        )

    def test_chukovsky(self):
        assert extract_author("Чуковский Корней - Детям. Стихи") == "Чуковский Корней"

    def test_krapivin(self):
        assert extract_author("Крапивин Владислав - Чоки-чок") == "Крапивин Владислав"

    def test_harris(self):
        assert (
            extract_author("Харрис Джоэль - Сказки дядюшки Римуса (Детское Радио)")
            == "Харрис Джоэль"
        )

    def test_belyanin(self):
        assert (
            extract_author("Белянин Андрей - Орден фарфоровых рыцарей (Детское Радио)")
            == "Белянин Андрей"
        )

    def test_bulychev(self):
        assert (
            extract_author("Булычев Кир - Сто лет тому вперед (2011)") == "Булычев Кир"
        )

    def test_defoe_brackets(self):
        assert (
            extract_author("Даниэль Дефо - Робинзон Крузо [Радиоспектакль]")
            == "Даниэль Дефо"
        )

    def test_dyachenko_en_dash(self):
        assert (
            extract_author(
                "Дяченко Марина и Сергей – Ключ от Королевства [Дина Бобылёва]"
            )
            == "Дяченко Марина и Сергей"
        )

    def test_lindgren(self):
        assert (
            extract_author("Линдгрен Астрид - Пеппи длинный Чулок") == "Линдгрен Астрид"
        )

    def test_grishkovets(self):
        assert extract_author("Гришковец - Как я съел собаку (2003)") == "Гришковец"

    def test_ermonlova(self):
        assert extract_author("Ермолова Елена - Волшебные краски") == "Ермолова Елена"

    def test_matyushkina_single(self):
        assert (
            extract_author("Матюшкина Екатерина - Кот да Винчи. Улыбка Анаконды")
            == "Матюшкина Екатерина"
        )

    def test_matyushkina_two_authors_comma(self):
        assert (
            extract_author(
                "Матюшкина Екатерина, Оковитая Екатерина - Ага, попался! (Детское Радио)"
            )
            == "Матюшкина Екатерина, Оковитая Екатерина"
        )

    def test_prokofieva(self):
        assert (
            extract_author("Прокофьева Софья - Девочка - свеча (Детское Радио)")
            == "Прокофьева Софья"
        )

    def test_ukrainian_names_single(self):
        assert (
            extract_author(
                "Юстасия Тарасава - Егорка и Змей Добрыныч [Детское радио, 2010]"
            )
            == "Юстасия Тарасава"
        )

    def test_ukrainian_names_two_authors_dot(self):
        assert (
            extract_author(
                "Чехонадский Александр. Ковальчук Юлия - Куса - пожиратель игрушек"
            )
            == "Чехонадский Александр. Ковальчук Юлия"
        )

    def test_sotnik(self):
        assert (
            extract_author(
                "Юрий Сотник - Машка Самбо и Заноза. Калуга - Марс [Детское радио, 2012]"
            )
            == "Юрий Сотник"
        )

    def test_filatov_uppercase(self):
        assert extract_author("ФИЛАТОВ - ФЕДОТ") == "ФИЛАТОВ"

    def test_hogarth(self):
        assert extract_author("Мафин и его веселые друзья. Э. Хогарт") == "Хогарт"


class TestExtractAuthorYearPrefix:
    """Pattern: YYYY - Author - Title (vinyl records)."""

    def test_1961_andersen(self):
        assert extract_author("1961 - Г.-Х. Андерсен - Дюймовочка") == "Г.-Х. Андерсен"

    def test_1969_bremen_no_second_dash(self):
        assert extract_author("1969 - Бременские музыканты") == "Бременские музыканты"

    def test_1970_pushkin(self):
        assert (
            extract_author("1970 - По щучьему велению - Русская народная сказка")
            == "По щучьему велению"
        )

    def test_1970_kipling(self):
        assert extract_author("1970 - Р.Киплинг - Рикки-Тикки-Тави") == "Р.Киплинг"

    def test_1986_nekrasov(self):
        assert (
            extract_author("1986 - А.Некрасов - Приключения капитана Врунгеля 2LP")
            == "А.Некрасов"
        )

    def test_1991_pushkin(self):
        assert (
            extract_author(
                "1991 - А.С.Пушкин - Сказка о мертвой царевне и семи богатырях"
            )
            == "А.С.Пушкин"
        )

    def test_1989_detektiv(self):
        assert (
            extract_author("1989 - Веселый детектив - Рок-опера для детей")
            == "Веселый детектив"
        )

    def test_1969_bremen_mixed(self):
        assert (
            extract_author("1969 - Бременские музыканты - track")
            == "Бременские музыканты"
        )


class TestExtractAuthorRoleBased:
    """Pattern: Title. Читает Author / Title. Исполняет Author."""

    def test_chitaet_litvinov_short(self):
        assert extract_author("Аленький цветочек. Читает Литвинов") == "Литвинов"

    def test_chitaet_luzhina_full_context(self):
        assert (
            extract_author("Баба-Яга. Русская народная сказка. Читает Лариса Лужина")
            == "Лариса Лужина"
        )

    def test_chitaet_luzhina_simple(self):
        assert extract_author("Загадки. Читает Лариса Лужина") == "Лариса Лужина"

    def test_chitaet_tabakov(self):
        assert (
            extract_author("Конек-Горбунок. Сказка Петра Ершова. Читает Олег Табаков")
            == "Олег Табаков"
        )

    def test_chitaet_vishnyakov(self):
        assert (
            extract_author("Зимовье зверей. Д. Мамин-Сибиряк, читает Петр Вишняков")
            == "Петр Вишняков"
        )

    def test_chitaet_freyndlikh(self):
        assert (
            extract_author("Маленький принц - Читает Алиса Фрейндлих")
            == "Алиса Фрейндлих"
        )

    def test_chitaet_ushpensky(self):
        assert extract_author("Чебурашка. Читает Э. Успенский") == "Э. Успенский"

    def test_chitaet_berestov_author_word(self):
        assert extract_author("Картинки в лужах. В.Берестов. Читает автор") == "автор"

    def test_ispolyaet_litvinov(self):
        assert (
            extract_author(
                "Волшебник Изумрудного города. Сказка. Исполняет Н. Литвинов"
            )
            == "Н. Литвинов"
        )


class TestExtractAuthorDotPattern:
    """Pattern: Title. Author (name after last dot)."""

    def test_nosov(self):
        assert extract_author("Автомобиль. Николай Носов") == "Николай Носов"

    def test_kashintsev(self):
        assert extract_author("Ёж и заяц. Игорь Кашинцев") == "Игорь Кашинцев"

    def test_yakovleva(self):
        assert extract_author("Белая уточка. Марина Яковлева") == "Марина Яковлева"

    def test_ivanov_hyphenated_title(self):
        assert extract_author("Волк-дурень. Борис Иванов") == "Борис Иванов"

    def test_pashutin(self):
        assert (
            extract_author("Василиса Прекрасная. Александр Пашутин")
            == "Александр Пашутин"
        )

    def test_rodonova(self):
        assert extract_author("Вор. Татьяна Родионова") == "Татьяна Родионова"

    def test_golyshev(self):
        assert extract_author("Война грибов с ягодами. Юрий Голышев") == "Юрий Голышев"

    def test_chernov(self):
        assert extract_author("Горе. Юрий Чернов") == "Юрий Чернов"

    def test_wilde(self):
        assert extract_author("Звездный мальчик. Оскар Уайльд") == "Оскар Уайльд"

    def test_emets(self):
        assert (
            extract_author("Властелин пыли. Музыкальная сказка-спектакль. Дмитрий Емец")
            == "Дмитрий Емец"
        )

    def test_bazhov_reversed(self):
        assert extract_author("Каменный цветок. Бажов Павел") == "Бажов Павел"

    def test_nosov_reversed(self):
        assert extract_author("Замазка. Носов Николай") == "Носов Николай"

    def test_rybnikov(self):
        assert extract_author("Буква Я. Алексей Рыбников") == "Алексей Рыбников"

    def test_balynt(self):
        assert extract_author("Гном-Гномыч и Изюмка. Балинт Агнеш") == "Балинт Агнеш"

    def test_initials_dotted(self):
        assert extract_author("Воробей. И.Тургеньев") == "И.Тургеньев"

    def test_kataev_initial(self):
        assert extract_author("Дудочка и Кувшинчик. В.Катаев") == "В.Катаев"

    def test_levin(self):
        assert (
            extract_author("Глупая Лошадь. В.Левин. Читает автор. Пять произведений")
            == "автор"
        )


class TestExtractAuthorDotWithGenrePrefix:
    """Pattern: Title. GenreWord Author (strip genre word before author)."""

    def test_andersen_after_skazka(self):
        assert (
            extract_author("Дикие лебеди. Сказка Ганса Христиана Андерсена")
            == "Ганса Христиана Андерсена"
        )

    def test_vvedensky_after_povest(self):
        assert (
            extract_author("Как Маша в саду испугалась. Повесть Александра Введенского")
            == "Александра Введенского"
        )

    def test_gauff_after_skazka(self):
        assert extract_author("Карлик Нос. Сказка В.Гауфа") == "В.Гауфа"

    def test_mikhailov_after_skazka(self):
        assert (
            extract_author("Два мороза. Сказка Михаила Михайлова")
            == "Михаила Михайлова"
        )

    def test_bazhov_after_skazka(self):
        assert (
            extract_author("Аилып и золотой волос. Сказка Павла Бажова")
            == "Павла Бажова"
        )

    def test_labule_after_skazka(self):
        assert extract_author("Зербино-дровосек. Сказка Э.Лабуле") == "Э.Лабуле"

    def test_gamara_after_skazka(self):
        assert extract_author("Волшебные слова. Сказка П.Гамарра") == "П.Гамарра"

    def test_biset_after_skazka(self):
        assert (
            extract_author("Как Поросенок учился летать. Сказка. Дональд Бисетт")
            == "Дональд Бисетт"
        )

    def test_odoevsky_after_skazka(self):
        assert (
            extract_author("Городок в табакерке. Сказка В.Одоевского") == "В.Одоевского"
        )

    def test_zhukovskaya_after_skazka(self):
        assert (
            extract_author("Как щенок был мамой. Сказка Е.Жуковской") == "Е.Жуковской"
        )


class TestExtractAuthorNoMatch:
    """Cases where no author should be extracted."""

    def test_genre_only(self):
        assert extract_author("Волшебная лампа Аладдина") == ""

    def test_folktale(self):
        assert extract_author("Волшебное колечко. Русская народная сказка") == ""

    def test_saying(self):
        assert extract_author("В стране невыученных уроков") == ""

    def test_kolobok(self):
        assert extract_author("Колобок. Сказка") == ""

    def test_collection(self):
        assert extract_author("Русские народные сказки") == ""

    def test_empty(self):
        assert extract_author("") == ""

    def test_musical_postanovka(self):
        assert extract_author("Беляночка и Розочка. Музыкальня постановка") == ""

    def test_musical_inscenirovka(self):
        assert extract_author("Бемби. Музыкальная инсценировка") == ""

    def test_radio_post(self):
        assert (
            extract_author(
                "Большая новость о Маленьком Мальчике. Фондовые записи радио"
            )
            == ""
        )

    def test_vinny_puh_union(self):
        assert (
            extract_author("Винни-Пух. \u201cСоюзмультфильм\u201d") == "Союзмультфильм"
        )

    def test_zhar_zhurnal(self):
        assert extract_author("Жила была песенка. Журнал Колобок") == "Колобок"

    def test_gulliver_reading(self):
        assert extract_author("Гулливер в стране лилипутов. Литературное чтение") == ""

    def test_afrika_narodnaya(self):
        assert extract_author("Женитьба зайца. Африканская сказка") == ""


class TestParseLine:
    """Full line parsing from real index.md entries."""

    def test_asimov_full(self):
        line = "- Айзек Азимов - 'Я - робот' [Радиоспектакль] | 4 4 MP3 | `AudioBooks/Айзек Азимов - 'Я - робот' [Радиоспектакль]/`"
        r = parse_line(line)
        assert r["title"] == "Айзек Азимов - 'Я - робот' [Радиоспектакль]"
        assert r["author"] == "Айзек Азимов"
        assert r["files"] == 4
        assert r["path"] == "AudioBooks/Айзек Азимов - 'Я - робот' [Радиоспектакль]/"

    def test_single_file(self):
        line = "- 38 Попугаев | 1 1 MP3 | `AudioBooks/Аудиосказки/Диск 1/38 Попугаев/`"
        r = parse_line(line)
        assert r["title"] == "38 Попугаев"
        assert r["files"] == 1
        assert r["author"] == ""

    def test_harry_potter_7(self):
        line = "- Книга 7 - Гарри Поттер и Дары Смерти | 160 160 MP3 | `AudioBooks/Роулинг Джоан Кэтлин - Гарри Поттер [Александр Клюквин]/Книга 7 - Гарри Поттер и Дары Смерти/`"
        r = parse_line(line)
        assert r["title"] == "Книга 7 - Гарри Поттер и Дары Смерти"
        assert r["files"] == 160
        assert r["author"] == ""

    def test_vinyl_flac(self):
        line = "- 1961 - Г.-Х. Андерсен - Дюймовочка | 1 1 FLAC | `AudioBooks/Детские пластинки/1961 - Г.-Х. Андерсен - Дюймовочка/`"
        r = parse_line(line)
        assert r["files"] == 1
        assert r["author"] == "Г.-Х. Андерсен"

    def test_mixed_format(self):
        line = "- 1969 - Бременские музыканты | 2 1 MP3, 1 FLAC | `AudioBooks/Детские пластинки/1969 - Бременские музыканты/`"
        r = parse_line(line)
        assert r["files"] == 2
        assert r["author"] == "Бременские музыканты"

    def test_two_flac(self):
        line = "- 1986 - А.Некрасов - Приключения капитана Врунгеля 2LP | 2 2 FLAC | `AudioBooks/Детские пластинки/1986 - А.Некрасов - Приключения капитана Врунгеля 2LP/`"
        r = parse_line(line)
        assert r["files"] == 2
        assert r["author"] == "А.Некрасов"

    def test_barto_24_poems(self):
        line = "- Агния Львовна Барто. Сказки и песни для детей. Игрушки. 24 Стиха | 24 24 MP3 | `AudioBooks/Аудиосказки/Диск 1/Агния Львовна Барто. Сказки и песни для детей. Игрушки. 24 Стиха/`"
        r = parse_line(line)
        assert r["files"] == 24
        assert (
            r["title"]
            == "Агния Львовна Барто. Сказки и песни для детей. Игрушки. 24 Стиха"
        )

    def test_deniskin(self):
        line = "- Денискины рассказы. Воздушный змей | 1 1 MP3 | `AudioBooks/Аудиосказки/Диск 1/Денискины рассказы. Воздушный змей/`"
        r = parse_line(line)
        assert r["title"] == "Денискины рассказы. Воздушный змей"
        assert r["files"] == 1
        assert r["author"] == ""

    def test_krylov_40(self):
        line = "- Басни Крылова. 40 басен | 40 40 MP3 | `AudioBooks/Аудиосказки/Диск 1/Басни Крылова. 40 басен/`"
        r = parse_line(line)
        assert r["files"] == 40

    def test_ushpensky_chitaet(self):
        line = "- Чебурашка. Читает Э. Успенский | 3 3 MP3 | `AudioBooks/Аудиосказки/Диск 3/Чебурашка. Читает Э. Успенский/`"
        r = parse_line(line)
        assert r["author"] == "Э. Успенский"
        assert r["files"] == 3

    def test_mamin_sibiryak(self):
        line = "- Зимовье зверей. Д. Мамин-Сибиряк, читает Петр Вишняков | 1 1 MP3 | `AudioBooks/Аудиосказки/Диск 2/Зимовье зверей. Д. Мамин-Сибиряк, читает Петр Вишняков/`"
        r = parse_line(line)
        assert r["author"] == "Петр Вишняков"

    def test_radio_theatre(self):
        line = "- Ауслендер Сергей - Ночной принц | 1 1 MP3 | `AudioBooks/Сборник радиоспектаклей №36 (1976 - 2012) MP3/Ауслендер Сергей  - Ночной принц/`"
        r = parse_line(line)
        assert r["author"] == "Ауслендер Сергей"

    def test_english_transliterated(self):
        line = "- 01-V strane Multi-Pulti | 16 16 MP3 | `AudioBooks/детские песенки 1-2/часть1/01-V strane Multi-Pulti/`"
        r = parse_line(line)
        assert r["title"] == "01-V strane Multi-Pulti"
        assert r["files"] == 16
        assert r["author"] == ""

    def test_collection_entry(self):
        line = "- Восточные сказки | 17 17 MP3 | `AudioBooks/Аудиосказки 2/Восточные сказки/`"
        r = parse_line(line)
        assert r["title"] == "Восточные сказки"
        assert r["files"] == 17
        assert r["author"] == ""

    def test_harry_potter_book1(self):
        line = "- Книга 1 - Гарри Поттер и Философский камень | 136 136 MP3 | `AudioBooks/Роулинг Джоан Кэтлин - Гарри Поттер [Александр Клюквин]/Книга 1 - Гарри Поттер и Философский камень/`"
        r = parse_line(line)
        assert r["files"] == 136
        assert r["author"] == ""

    def test_not_entry_header(self):
        assert parse_line("## AudioBooks/") is None

    def test_not_entry_table(self):
        assert parse_line("| Category | Dirs | MP3 | FLAC | Files |") is None

    def test_not_entry_empty(self):
        assert parse_line("") is None

    def test_not_entry_hr(self):
        assert parse_line("---") is None
