# Quick Reference

| Annotation                        | Description                         | Example                      |
|-----------------------------------|-------------------------------------|------------------------------|
| `int`, `str`, `float`, `bool`     | Basic built-in types                | `age: int = 25`              |
| `List[T]`, `list[T]`              | List containing items of type `T`   | `scores: list[int]`          |
| `Tuple[T, ...]`                   | Tuple with specified item types     | `coords: tuple[float, float]`|
| `Dict[K, V]`, `dict[K, V]`        | Dictionary with keys `K`, values `V`| `user_data: dict[str, int]`  |
| `Set[T]`, `set[T]`                | Set containing items of type `T`    | `tags: set[str]`             |
| `Optional[T]`                     | Type `T` or `None`                  | `name: Optional[str]`        |
| `Union[T1, T2]` or `T1 | T2`      | Either type `T1` or `T2`            | `value: int | str`           |
| `Callable[[Args], ReturnType]`    | Function types                      | `adder: Callable[[int, int], int]` |
| `Literal["value"]`                | Specific literal values             | `mode: Literal["auto", "manual"]` |
| `Annotated[T, metadata]`          | Type `T` with additional metadata   | `UserID = Annotated[int, "primary key"]` |
| `NewType('Name', T)`              | New distinct type based on type `T` | `UserId = NewType('UserId', int)`|
| `Protocol`                        | Structural typing protocol          | `class Speaker(Protocol): ...`|
