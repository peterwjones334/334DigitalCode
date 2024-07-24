from ldap3 import Server, Connection, ALL, MOCK_SYNC, Entry, Attribute, ObjectDef, Reader, MOCK_ASYNC
from ldap3.utils.mocked import MockStrategy

# Define basic attributes for LDAP entries
attributes = ['displayName', 'mail', 'sip']

# Create a mock LDAP server
server = Server('my_mock_server', get_info=ALL)

# Use the mock strategy for the server
server.strategy = MockStrategy()
server.strategy.sync = False
server.strategy.open()

# Define an object class for our entries
person_object_def = ObjectDef(['inetOrgPerson', 'person'], server)

# Create a connection to the mock server
conn = Connection(server, client_strategy=MOCK_ASYNC)
conn.bind()
conn.strategy.add_entry('cn=my_admin,dc=example,dc=com', {'userPassword': 'mypassword', 'sn': 'admin_sn', 'cn': 'my_admin'})

# Function to add an entry
def add_entry(dn, attributes):
    entry = Entry(dn, person_object_def)
    for attr, value in attributes.items():
        entry[attr] = Attribute(person_object_def[attr])
        entry[attr].value = value
    conn.strategy.add_entry(entry.entry_to_ldif())
    print(f"Added entry: {dn}")

# Function to search for entries
def search_entry(filter):
    reader = Reader(conn, person_object_def, 'dc=example,dc=com', filter)
    reader.search()
    for entry in reader.entries:
        print(entry)

# Adding an example entry
dn = 'cn=John Doe,dc=example,dc=com'
attributes = {
    'displayName': 'John Doe',
    'mail': 'john.doe@example.com',
    'sip': 'john.doe@sip.example.com'
}
add_entry(dn, attributes)

# Searching for the entry
search_entry('(displayName=John Doe)')

# Unbind the connection
conn.unbind()
