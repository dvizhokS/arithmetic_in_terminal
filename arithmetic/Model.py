import sqlite3


class Model:
    db_name = "arithmetic.db"
    table_name = "example"
    con = None
    cur = None
    is_example_exist = False
    where_string = None
    insert_value_string = None
    update_value_string = None

    def __init__(self):
        self.con = sqlite3.connect(self.db_name)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.create_table(self.table_name)

    def create_table(self, table_name):
        sql = ("CREATE TABLE IF NOT EXISTS " +
               table_name +
               (" "
                "(id INTEGER primary KEY, "
                "x INTEGER, "
                "y INTEGER, "
                "sign char, "
                "ans INTEGER, "
                "status boolean, "
                "times INTEGER)"
                ))
        self.cur.execute(sql)
        self.con.commit()

    def set_table(self, table_name):
        self.table_name = table_name

    def get_example(self, **kwargs):
        self.where_prepare(**kwargs)

        sql = "SELECT * from {} WHERE {}".format(self.table_name, self.where_string)
        # print(sql)
        res = self.cur.execute(sql)
        example = res.fetchone()

        if example is None:
            self.is_example_exist = False
            return False

        self.is_example_exist = True
        return example

    def get_example_not_solved(self):
        sql = "SELECT * from {} WHERE {} LIMIT 1".format(self.table_name, "status = 0")
        res = self.cur.execute(sql).fetchone()
        if res is None:
            return False
        self.where_prepare(id=res['id'])
        return res

    def get_slow_example(self):
        sql = "SELECT * from {} Order By times DESC LIMIT 1".format(self.table_name)
        res = self.cur.execute(sql).fetchone()
        if res is None:
            return False
        self.where_prepare(id=res['id'])
        return res

    def insert_data(self, **kwargs):
        example = self.get_example(**kwargs)
        if not example:
            # print("Not example")
            self.insert_values_prepare(**kwargs)
            sql = "INSERT INTO {table} {values}".format(table=self.table_name, values=self.insert_value_string)
            self.cur.execute(sql)
            self.con.commit()

    # def update_data(self, **kwargs):

    def update_data(self, **kwargs):
        self.update_values_prepare(**kwargs)
        sql = ("UPDATE {table} SET {values} Where {where}".
               format(table=self.table_name, values=self.update_value_string, where=self.where_string))
        self.cur.execute(sql)
        self.con.commit()

    def where_prepare(self, **where_list):
        where = self.key_value_prepare_list(**where_list)
        self.where_string = " and ".join(where)

    def insert_values_prepare(self, **values_list):
        column, value = self.value_prepare(**values_list)
        self.insert_value_string = "({}) VALUES ({})".format(", ".join(column), ", ".join(value))

    def update_values_prepare(self, **values_list):
        values = self.key_value_prepare_list(**values_list)
        self.update_value_string = ", ".join(values)

    def value_prepare(self, **values_list):
        column = []
        value = []

        for k, v in values_list.items():
            if type(v) == str:
                v = "'{}'".format(v)
            else:
                v = str(v)
            column.append(k)
            value.append(v)
        return column, value

    def key_value_prepare_list(self, **kwargs):
        key_value = []

        for k, v in kwargs.items():
            if type(v) == str:
                v = "'{}'".format(v)
            key_value.append("{} = {}".format(k, v))
        return key_value

