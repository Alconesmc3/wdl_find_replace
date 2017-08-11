# import unittest
# import FindWdlReplaceJson
#
# class TestFindWdlReplaceJson(unittest.TestCase):
#     def test_FindAllWdlVarInLine(self):
#         expected_list = TestFindWdlReplaceJson.FindAllWdlVarInLine("${sampleName}_raw.${type}.vcf")
#         assert expected_list == ['sampleName', 'type']
#
#     def test_NonRepeatWdlVarList(self):
#         result_list = TestFindWdlReplaceJson.NonRepeatWdlVarList("/home/math/Desktop/ucsc/WDL_tutorials_me_July2017/jointCallingGenotypes.wdl")
#         assert result_list == ['sampleName', 'sep=" -V " GVCFs', 'bamFile', 'RefFasta', 'GATK']
#
#!/usr/bin/env python2

# 2017 Lon Blauvelt

import unittest

from FindWdlReplaceJson import FindWdlReplaceJsonPath

class TestCase(unittest.TestCase):
    """A set of test cases for fence_class.py"""

    def setUp(self):
        """
        Initial set up of variables for the test.  Three test files are
        provided (must be in the same folder).
        """

        self.i = FindWdlReplaceJsonPath()

    def tearDown(self):
        """Default tearDown for unittest."""
        unittest.TestCase.tearDown(self)

    def testFindAllWdlVarInLine(self):
        line_in_file = 'iashfiuhsdiu${helloworld}fhui'
        true_line_output = ['helloworld']
        returned_line = self.i.FindAllWdlVarInLine(line_in_file)
        assert true_line_output == returned_line, "FindAllWdlVarInLine function is not returning the variables properly."
        # print(returned_line)
    #
    def testNonRepeatWdlVarList(self):
        wdl_file_test = "/home/math/Desktop/ucsc/WDL_tutorials_me_July2017/jointCallingGenotypes.wdl"
        wdl_var_no_repeats = ['sampleName', 'sep=" -V " GVCFs', 'bamFile', 'RefFasta', 'GATK']
        returned_variables = self.i.NonRepeatWdlVarList(wdl_file_test)
        assert wdl_var_no_repeats == returned_variables , "testNonRepeatWdlVarList function is not returning the correct variables"

    def testJsonListAndDictToPath(self):
        json_file_test = "/home/math/Desktop/ucsc/WDL_tutorials_me_July2017/jointCallingGenotypes_inputs.json"
        jlist_var2path = ([u'refFasta', u'gatk', u'refDict', u'refIndex', u'inputSamplesFile'],
{u'refIndex': u'/home/math/Desktop/jointCallingGenotypes/ref/human_g1k_b37_20.fasta.fai', u'inputSamplesFile': u'/home/math/Desktop/inputsTSV.txt', u'refDict': u'/home/math/Desktop/jointCallingGenotypes/ref/human_g1k_b37_20.dict', u'refFasta': u'/home/math/Desktop/jointCallingGenotypes/ref/human_g1k_b37_20.fasta', u'gatk': u'/home/math/Desktop/GenomeAnalysisTK.jar'})
        returned_jlist_var2path = self.i.JsonListAndDictToPath(json_file_test)
        assert jlist_var2path == returned_jlist_var2path , "testJsonListAndDictToPath function is not returning the correct list and dictionary"

    def testCompareVarCreateDict(self):
        json_file_test = "/home/math/Desktop/ucsc/WDL_tutorials_me_July2017/jointCallingGenotypes_inputs.json"
        self.i.JsonListAndDictToPath(json_file_test)
        match_wdl2json_dict = {'${GATK}': u'gatk', '${RefFasta}': u'refFasta'}
        returned_dict = self.i.CompareVarCreateDict(['sampleName', 'sep=" -V " GVCFs', 'bamFile', 'RefFasta', 'GATK'])
        assert match_wdl2json_dict == returned_dict , "CompareVarCreateDict function is not returning the right dictionary."

    def testRemoveMatchedVarList(self):
        wdl_file_test = "/home/math/Desktop/ucsc/WDL_tutorials_me_July2017/jointCallingGenotypes.wdl"
        json_file_test = "/home/math/Desktop/ucsc/WDL_tutorials_me_July2017/jointCallingGenotypes_inputs.json"
        no_repeat_wdl = self.i.NonRepeatWdlVarList(wdl_file_test)
        self.i.JsonListAndDictToPath(json_file_test)
        self.i.CompareVarCreateDict(no_repeat_wdl)
        final_matches_removed = ['sampleName', 'sep=" -V " GVCFs', 'bamFile'],[u'refDict', u'refIndex', u'inputSamplesFile']
        returned_unmatched_lists = self.i.RemoveMatchedVarList(no_repeat_wdl)
        assert final_matches_removed == returned_unmatched_lists, "RemoveMatchedVarList is not returning the right two lists"

    def testMatchSimilarVarLCSFourAndUP(self):
        wdl_file_test = "/home/math/Desktop/ucsc/WDL_tutorials_me_July2017/jointCallingGenotypes.wdl"
        json_file_test = "/home/math/Desktop/ucsc/WDL_tutorials_me_July2017/jointCallingGenotypes_inputs.json"
        no_repeat_wdl = self.i.NonRepeatWdlVarList(wdl_file_test)
        self.i.JsonListAndDictToPath(json_file_test)
        self.i.CompareVarCreateDict(no_repeat_wdl)
        self.i.RemoveMatchedVarList(no_repeat_wdl)
        final_w2j_dict_jvar_no = ({'${GATK}': u'gatk', '${sampleName}': u'inputSamplesFile', '${RefFasta}': u'refFasta'}, [u'refDict', u'refIndex'])
        returned_dict_list = self.i.MatchSimilarVarLCSFourAndUP(no_repeat_wdl)
        assert final_w2j_dict_jvar_no == returned_dict_list, "MatchSimiliarVarLCSFourAndUp is not returning the right dictionary and list"

    def NewFileWithReplacements(self):
        wdl_file_test = "/home/math/Desktop/ucsc/WDL_tutorials_me_July2017/jointCallingGenotypes.wdl"
        json_file_test = "/home/math/Desktop/ucsc/WDL_tutorials_me_July2017/jointCallingGenotypes_inputs.json"
        no_repeat_wdl = self.i.NonRepeatWdlVarList(wdl_file_test)
        self.i.JsonListAndDictToPath(json_file_test)
        self.i.CompareVarCreateDict(no_repeat_wdl)
        self.i.RemoveMatchedVarList(no_repeat_wdl)
        self.i.MatchSimilarVarLCSFourAndUP(no_repeat_wdl)
        final_wdl_file =  "/home/math/Desktop/ucsc/WDL_tutorials_me_July2017/jointCallingGenotypes_copy.wdl"  #is it possible to put something like: wdl_file_test.replace(".wdl", "_copy.wdl")?
        returned_edit_wdl = self.i.NewFileWithReplacements(wdl_file_test)
        assert final_wdl_file == returned_edit_wdl , "FileWithReplacements is not returning the correct file with all replacements"





