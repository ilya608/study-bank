# def get_regions_data(self, region):
#     cursor = self.connection.cursor()
#
#     query = f'''SELECT regions, population, salary, population_density, happy_index
#             FROM regions_table WHERE regions = {region}'''
#
#     cursor.execute(query)
#     result = cursor.fetchall()
#
#     self.connection.commit()
#     cursor.close()
#
#     return {'population': result[0][1],
#             'salary': row[0][2],
#             'population_density': row[0][3],
#             'happy_index': row[0][4]}