namespace Dotnet10.Domain;

/// <summary>
/// Composite primary key value object.
/// Equivalent to @Embeddable StoreFruitPriceId in the Quarkus project.
/// </summary>
public record StoreFruitPriceId(long StoreId, long FruitId)
{
    public StoreFruitPriceId(Store store, Fruit fruit) : this(store.Id, fruit.Id) { }
}
