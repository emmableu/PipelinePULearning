# import sys
# from Costume import *
# from VariableFrame import *
# class Scriptable:
#     def read_sb3(self, json_obj, project, library_index):
#         costume_obj_s = json_obj['costumes']
#         self.project = project
#         self.name = json_obj['name'] #e.g. json_obj['targets'][0]['name'] = 'Stage'
#         self.costume_s = []
#         for costume_obj in costume_obj_s:
#             self.costume_s.append(Costume(costume_obj, project))
#         self.costume_index = json_obj['currentCostume']+1
