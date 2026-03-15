# dotnet10

.NET 10 / ASP.NET Core counterpart of the `quarkus3` project, built for framework performance comparisons.

## How to run `stress.sh`?

1. Install .NET (see Prerequisites)
2. Compile to managed mode with `dotnet publish Dotnet10 -c Release -o publish`
   (see Managed mode)
3. From the Git project root run `./scripts/stress.sh dotnet10`

## Prerequisites

### .NET 10 SDK

#### Linux

**Ubuntu / Debian**

```bash
sudo apt-get update && sudo apt-get install -y dotnet-sdk-10.0
```

If the package is not found, register the Microsoft package feed first:

```bash
wget https://packages.microsoft.com/config/ubuntu/24.04/packages-microsoft-prod.deb \
     -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb && rm packages-microsoft-prod.deb
sudo apt-get update && sudo apt-get install -y dotnet-sdk-10.0
```

**Fedora / RHEL / CentOS**

```bash
sudo dnf install dotnet-sdk-10.0
```

#### macOS

```bash
brew install dotnet@10
```

Or download the `.pkg` installer from <https://dotnet.microsoft.com/en-us/download/dotnet/10.0>.

#### Windows

```powershell
winget install Microsoft.DotNet.SDK.10
```

Or download the `.exe` installer from <https://dotnet.microsoft.com/en-us/download/dotnet/10.0>.

#### Verify

```bash
dotnet --version   # should print 10.x.x
```

## Database

PostgreSQL on `localhost:5432`, database `fruits`, user `fruits`, password `fruits`.

## Managed mode

Compiles to platform-neutral IL that runs on the installed .NET runtime.
Equivalent to `./mvnw clean package` + `java -jar target/quarkus-app/quarkus-run.jar` in the Quarkus project.

```bash
dotnet publish Dotnet10 -c Release -o publish
./publish/dotnet10
```

The server listens on **http://localhost:8080**, matching the Quarkus default.

## Native mode

**Not supported.** This project cannot be compiled to a native binary with the current
version of EF Core. The managed-mode binary (`dotnet publish -c Release`) is the valid
comparison point against the Quarkus JVM build.

### Why NativeAOT does not work with EF Core

.NET NativeAOT compiles the entire application to a self-contained native binary at
build time. At runtime there is no JIT compiler and no dynamic code generation of any
kind. EF Core relies on both in two separate places:

**Problem 1 — model building.** At startup, EF Core reflects over entity classes,
reads annotations, and builds an `IModel` that describes the full database schema.
This process uses reflection APIs that the AOT linker removes, producing:

```txt
InvalidOperationException: Model building is not supported when publishing with NativeAOT.
```

**Problem 2 — LINQ query translation.** At runtime, every LINQ query (`.Where()`,
`.OrderBy()`, `.Include()`) is compiled from an expression tree into SQL using
`System.Reflection.Emit`. This is dynamic code generation, which NativeAOT forbids:

```txt
InvalidOperationException: Query wasn't precompiled and dynamic code isn't supported (NativeAOT).
```

### Why the existing workarounds did not work

EF Core 9 ships two partial solutions:

- **`dotnet ef dbcontext optimize`** pre-generates the model as static C# files,
  solving Problem 1. This worked.
- **`Microsoft.EntityFrameworkCore.Tasks`** is a build-time source generator that is
  supposed to emit SQL interceptors for LINQ queries, solving Problem 2. In practice it
  failed on every query — including bare `context.Stores.ToListAsync()` — with
  *"Dynamic LINQ queries are not supported when precompiling queries"*.

Replacing EF Core with raw Npgsql SQL would fix the runtime errors but destroy the
comparability of the benchmark: the whole point is to compare equivalent ORM-based
stacks. If .NET uses raw SQL, Quarkus would have to use raw SQL too.

### Why Quarkus native image works

The Quarkus team ships a complete GraalVM native-image configuration for Hibernate ORM
and RESTEasy as part of the framework extensions. Query translation, model building, and
reflection metadata are all handled at build time through Quarkus's own
bytecode-transformation infrastructure. This is years of framework-level investment that
has no equivalent in the .NET ecosystem yet.

### What to expect in future versions

EF Core's roadmap includes full NativeAOT support. The pieces being developed are:

- **Compiled models** (`dotnet ef dbcontext optimize`) — already working in EF Core 8+.
- **Precompiled queries** via C# interceptors — introduced as experimental in EF Core 9,
  currently limited to simple queries without navigation property loading.
- **Full `Include` support** in the precompiler — planned for a future EF Core release
  once the interceptor infrastructure matures.

When precompiled queries fully support navigation properties and eager loading, native
compilation of this project should become possible without any code changes beyond
running `dotnet ef dbcontext optimize` and `dotnet publish -p:PublishAot=true`.

## Development

```bash
dotnet run --project Dotnet10
```

## Test

The test suite has three levels, matching the Quarkus test structure:

### Unit tests (`Service/FruitServiceTests`)

Tests `FruitService` directly with a hand-written fake repository. No database or running
application required. Equivalent to `@QuarkusTest FruitControllerTests` in the Quarkus project.

```bash
dotnet test --filter "FullyQualifiedName~Service"
```

### End-to-end tests (`E2e/FruitControllerEndToEndTest`)

Tests the full HTTP API of the running application. Equivalent to
`@QuarkusIntegrationTest FruitControllerIT` in the Quarkus project. Requires the
application to be running (`dotnet run --project Dotnet10`) and the database
seeded from `import.sql` before the tests are started. Seeding the database is
best done using `../script/infra.sh -s`.

```bash
dotnet test --filter "FullyQualifiedName~E2e"
```

### Run all tests

```bash
dotnet test
```

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/fruits` | All fruits with store prices |
| GET | `/fruits/{name}` | Single fruit or 404 |
| POST | `/fruits` | Create a new fruit |
| GET | `/health/live` | Liveness probe |
| GET | `/health/ready` | Readiness probe (includes DB check) |
| GET | `/metrics` | Prometheus metrics |

## Architecture comparison with quarkus3

| Concern | Quarkus 3 | dotnet10 |
|---------|-----------|----------|
| HTTP layer | `quarkus-rest-jackson` / JAX-RS `@Path` | ASP.NET Core Minimal API (`MapGet` / `MapPost`) |
| ORM | Hibernate ORM + Panache | EF Core 10 + Npgsql |
| Embedded value object | `@Embeddable` / `@Embedded` | `[Owned]` (EF Core owned type) |
| Composite PK | `@EmbeddedId` / `@MapsId` | `HasKey(e => new { e.StoreId, e.FruitId })` |
| Eager fetch | `FetchType.EAGER` + `@Fetch(SELECT)` | `.Include().ThenInclude()` in repository |
| Natural ID / unique key | `@NaturalId` | `HasIndex(x => x.Name).IsUnique()` |
| DI scope | `@ApplicationScoped` (CDI) | `AddScoped()` (ASP.NET Core DI) |
| Bean Validation | `jakarta.validation` annotations | DataAnnotations + `[ApiController]` auto-400 |
| Health checks | `quarkus-smallrye-health` | `AddHealthChecks()` + `AddDbContextCheck<T>()` |
| Metrics | `quarkus-micrometer-registry-prometheus` | `prometheus-net.AspNetCore` |
| JSON null handling | `serialization-inclusion: non-empty` | `JsonIgnoreCondition.WhenWritingNull` |
| Reflection-free JSON | `enable-reflection-free-serializers: true` | `[JsonSerializable]` source-generated `FruitJsonContext` |
| AOT build flag | `./mvnw clean package -Pnative` | Not supported – EF Core LINQ translator requires dynamic code |
| AOT output | `target/app-runner` (GraalVM native image) | Not available (see Native mode section) |
| Unit test framework | JUnit 5 + `@QuarkusTest` | xUnit |
| Unit test mock | `@InjectMock` (Mockito) | Hand-written `FakeFruitRepository` |
| Unit test target | `FruitController` via HTTP | `FruitService` directly |
| Repository tests | `@TestTransaction` rollback | Covered by E2E tests (no separate process needed) |
| E2E tests | `@QuarkusIntegrationTest` (separate process) | `HttpClient` against running app |
| Test ordering | `@TestMethodOrder` + `@Order` | `PriorityOrderer` + `[TestPriority]` |
