using Dotnet10;
using Dotnet10.Data;
using Dotnet10.Dto;
using Dotnet10.Repository;
using Dotnet10.Service;
using Microsoft.EntityFrameworkCore;
using Prometheus;

var builder = WebApplication.CreateSlimBuilder(args);

builder.Services.ConfigureHttpJsonOptions(options =>
    options.SerializerOptions.TypeInfoResolverChain.Insert(0, FruitJsonContext.Default));

// ── Database ──────────────────────────────────────────────────────────────────
// Equivalent to quarkus-jdbc-postgresql + quarkus-hibernate-orm-panache.
// Read the connection string from configuration when available (development),
// fall back to the hardcoded default so the published binary works without
// appsettings.json being present in the working directory.
var connectionString =
    builder.Configuration.GetConnectionString("DefaultConnection")
    ?? "Host=localhost;Port=5432;Database=fruits;Username=fruits;Password=fruits";

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(connectionString));

// ── Application Services ──────────────────────────────────────────────────────
// Equivalent to @ApplicationScoped CDI beans in Quarkus.
builder.Services.AddScoped<IFruitRepository, FruitRepository>();
builder.Services.AddScoped<FruitService>();

// ── Health checks ─────────────────────────────────────────────────────────────
// Equivalent to quarkus-smallrye-health.
builder.Services.AddHealthChecks()
    .AddDbContextCheck<AppDbContext>();

// Bind to port 8080 to match the Quarkus default.
// Set in code so it applies to the published binary even without appsettings.json.
builder.WebHost.UseUrls("http://0.0.0.0:8080");

var app = builder.Build();

// ── Metrics ───────────────────────────────────────────────────────────────────
// Equivalent to quarkus-micrometer-registry-prometheus.
app.UseHttpMetrics();
app.MapMetrics("/metrics");

// ── Fruit endpoints ───────────────────────────────────────────────────────────
// Minimal API. Equivalent to @Path("/fruits") FruitController in the Quarkus project.
var fruits = app.MapGroup("/fruits");

fruits.MapGet("/", async (FruitService svc) =>
    Results.Ok(await svc.GetAllFruitsAsync()));

fruits.MapGet("/{name}", async (string name, FruitService svc) =>
{
    var fruit = await svc.GetFruitByNameAsync(name);
    return fruit is null ? Results.NotFound() : Results.Ok(fruit);
});

fruits.MapPost("/", async (FruitDto dto, FruitService svc) =>
    Results.Ok(await svc.CreateFruitAsync(dto)));

// ── Health endpoints ──────────────────────────────────────────────────────────
app.MapHealthChecks("/health/live");
app.MapHealthChecks("/health/ready");

app.Run();
