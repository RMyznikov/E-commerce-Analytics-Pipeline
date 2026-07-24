from app.generator.generate_dataset import DatasetConfig, DatasetGenerator


class EcommerceAnalyticsPipeline:
    def main(self) -> None:
        test_config = DatasetConfig(
            customers=2,
            products=2,
            orders=2,
            order_items=2,
            seed=2,
        )
        paths = DatasetGenerator(test_config).generate()
        for name, path in paths.items():
            print(f"{name}: {path}")


if __name__ == "__main__":
    e_commerce_pipeline = EcommerceAnalyticsPipeline()
    e_commerce_pipeline.main()

