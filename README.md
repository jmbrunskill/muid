# muID - User Readable & Application Specific Unique IDs

In modern cloud based applications and distributed systems, a reliable mechanism of creating unique IDs is required.
Standards such as RFC4122 Allow software Globally Unique UUIDs with almost 0% chance of a collision. See: (https://tools.ietf.org/html/rfc4122) or (https://en.wikipedia.org/wiki/Universally_unique_identifier)

This standard attempts to create a alternative mechanism for creating shorter 64bit ids which might be more useful for application specific purposes.

## Why create this?

As a developer working with UUID's can be frustrating and hard to reason about.
Lets say in your database you have 2 ids `e9bdd14e-a796-11e9-a2a3-2a2ae2dbcce4` and `e9bdd4c8-a796-11e9-a2a3-2a2ae2dbcce4`

If in your debugging code you the id `e9bdd4c8-a796-11e9-a2a3-2a2ae2dbcce4` it's much harder for a developer to differentiate.

With muID's in most cases you'll only have to look at the last 4-6 characters to differentiate ids in context. `5d2cfc97-58-e7-57` vs `5d2cfc98-5d-1d-fe`

Additionally this format allows you use a normal BIGINT (64bit) datatype in your database, which m your db queries & joins more efficent.

## When *not* to use this
* If you application is expecting to consistently create 100's or 1000's of ids per second
* If you have a number of machines or threads generating ids concurrently
* If you need to use an internationally recognised standard

## When should I use this?
* If you have a relatively slow moving application which needs to generate ids without central co-ordination
* You want an id that's more easily recognised by a human
* You don't need to generate huge numbers of ids (Libraries may deliberately rate limit id creation)
* You value shorter id sizes (eg. send less bits across a network etc)

## Alternatives
_Have you heard about twitter snowflake or boundry flake?_
Yes. It's fair to say I was inspired by these types of uuid generators.
However this standard focuses on readability over speed and robustness.

## Why is is called muID?
mu stands for the greek letter 'μ' it represents the relative 'smallness' 

## Is it in production?
No, not yet. Let me know if you are using this in a production use case?

## The Nitty Gritty

The muID format is formed using optional key'd strings these allow the creator of the id to have some control over how an id is created.

SOURCE_KEY - This is intended to represent a datasource, server, site etc - This should be different for different generation sources
This key will be hashed and the lower bits of this hash used to create the 8bit SOURCEID.
Note: If this is not provided library should substitute some kind of host id (MAC Address for example)

ITEM_KEY - This is intended to represent something likely to be unique about item being identified, eg a Name
This key will be hashed and the lower bits of this hash used to create the 8bit ITEMID.
Note: If this is not provided by the caller, a library should substitute some kind of independantly incrementing or random number

The muid generator should keep an incrementing integer in it's internal state. 
This is known as 'SEQ'
This allows for up to 65536 id's to be created from the same source in the same second without conflicts.
A more sophisticated algorithm could keep a seq number per source_id or item_id (or both) potentially allowing even more ids without a conflict. This makes is suitable for batch processing of ids (eg. generating 10000+ of ids per second if they are keyed with a relevent itemid)

The muID binary format is formed like this:
|<UNIXTIMESTAMP>[32bits]<SOURCEID>[8bits]<ITEMID>[8bits]<SEQ>[16bits]|

A string representation of the muID should be in hex format with '-' characters separating the fields UNIXTIMESTAMP-SOURCEID-ITEMID-SEQ
Hex Strings should **not** be 0 padded, thus making it easier to read eg. `1d-fe` is easier to read than `1d-00fe`

Examples ID's
* `int(6714026395928297728),str(5d2d036f-45-e7-100)`
* `int(6714026738942017537), str(5d2d03bf-23-1d-1)`


## Is this format resilient against clock drift?
Not really. We assume that this case is rare, and that the internal seq state will minimise the chance of a clock drift collision.

### Example Implementations

Note: These implementations are provided as examples only. Your own milage my vary using these.
* Python


## Authors

* **James Brunskill** - *Initial work* - [jmbrunskill](https://github.com/jmbrunskill)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details