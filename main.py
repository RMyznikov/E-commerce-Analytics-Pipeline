from src.generator.customers_csv_generator import CustomersCsvGenerator


class eCommerceAnaliticsPipeline:
    def __init__(self):
        pass

    def main(self):
        result = CustomersCsvGenerator.generate_test_csv(100)
        print(result)


if __name__ == '__main__':
    e_commerce_pipeline = eCommerceAnaliticsPipeline()
    e_commerce_pipeline.main()

