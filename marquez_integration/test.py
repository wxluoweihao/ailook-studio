from marquez_integration.marquez_lineage_collector import MarquezLineageCollector


def main():
    collector = MarquezLineageCollector(host="8.210.27.71:45432",
                                        database="marquez",
                                        user="marquez-user",
                                        password="mZ7J1F4IYqY6mbIY53Jgu1aL9lqpfjtjdJ5zMRjz9yoC0rL02cweCopEXans2gr4")

    lineagesLists = collector.generate_lineages()

    print(lineagesLists)
if __name__ == "__main__":
    main()
