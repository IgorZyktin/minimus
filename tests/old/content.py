REF_MD = r"""
# Слон

Большое млекопитающие.

---
\#хобот
[\#4 лапы](./meta_4_lapy.md)
[\#серый](./meta_seryy.md)
\#большой

Живёт в Африке и Индии \#большой.
""".strip()

REF_MD_WITH_LINKS = r"""
# Слон

Большое млекопитающие.

---
[\#хобот](./meta_hobot.md)
[\#4 лапы](./meta_4_lapy.md)
[\#серый](./meta_seryy.md)
[\#большой](./meta_bolshoy.md)

Живёт в Африке и Индии [\#большой](./meta_bolshoy.md).
""".strip()

REF_METAFILE_MD = """
## Все вхождения тега "ultra"

---


1 из 2. [Title 1](./a.txt)

2 из 2. [Title 2](./b.txt)

""".lstrip()
