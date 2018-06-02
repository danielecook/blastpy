import requests


NCBI_BLAST_URL = "https://blast.ncbi.nlm.nih.gov/Blast.cgi" 


class blast:

    def __init__(self, program, database='ncbi'):
        assert program in ['blastn', 'blastp', 'blastx', 'tblastn', 'tblastx'] 
        self.program = program
        self.database = database



    def query(sequence,
              url_base=NCBI_BLAST_URL, 
              auto_format=None,
              composition_based_statistics=None,
              db_genetic_code=None,
              endpoints=None,
              entrez_query='(none)', 
              expect=10.0,
              filter=None,
              gapcosts=None,
              genetic_code=None, 
              hitlist_size=50,
              i_thresh=None,
              layout=None,
              lcase_mask=None, 
              matrix_name=None,
              nucl_penalty=None,
              nucl_reward=None, 
              other_advanced=None,
              perc_ident=None,
              phi_pattern=None, 
              query_file=None,
              query_believe_defline=None,
              query_from=None, 
              query_to=None,
              searchsp_eff=None,
              service=None,
              threshold=None, 
              ungapped_alignment=None,
              word_size=None, 
              alignments=500,
              alignment_view=None,
              descriptions=500, 
              entrez_links_new_window=None,
              expect_low=None, expect_high=None, 
              format_entrez_query=None,
              format_object=None, format_type='XML', 
              ncbi_gi=None,
              results_file=None,
              show_overview=None,
              megablast=None, 
              template_type=None,
              template_length=None):
   
   
      # Format the "Put" command, which sends search requests to qblast. 
      # Parameters taken from http://www.ncbi.nlm.nih.gov/BLAST/Doc/node5.html on 9 July 2007 
      # Additional parameters are taken from http://www.ncbi.nlm.nih.gov/BLAST/Doc/node9.html on 8 Oct 2010 
      # To perform a PSI-BLAST or PHI-BLAST search the service ("Put" and "Get" commands) must be specified 
      # (e.g. psi_blast = NCBIWWW.qblast("blastp", "refseq_protein", input_sequence, service="psi")) 
      parameters = [ 
          ('AUTO_FORMAT', auto_format), 
          ('COMPOSITION_BASED_STATISTICS', composition_based_statistics), 
          ('DATABASE', database), 
          ('DB_GENETIC_CODE', db_genetic_code), 
          ('ENDPOINTS', endpoints), 
          ('ENTREZ_QUERY', entrez_query), 
          ('EXPECT', expect), 
          ('FILTER', filter), 
          ('GAPCOSTS', gapcosts), 
          ('GENETIC_CODE', genetic_code), 
          ('HITLIST_SIZE', hitlist_size), 
          ('I_THRESH', i_thresh), 
          ('LAYOUT', layout), 
          ('LCASE_MASK', lcase_mask), 
          ('MEGABLAST', megablast), 
          ('MATRIX_NAME', matrix_name), 
          ('NUCL_PENALTY', nucl_penalty), 
          ('NUCL_REWARD', nucl_reward), 
          ('OTHER_ADVANCED', other_advanced), 
          ('PERC_IDENT', perc_ident), 
          ('PHI_PATTERN', phi_pattern), 
          ('PROGRAM', program), 
          # ('PSSM',pssm), - It is possible to use PSI-BLAST via this API? 
          ('QUERY', sequence), 
          ('QUERY_FILE', query_file), 
          ('QUERY_BELIEVE_DEFLINE', query_believe_defline), 
          ('QUERY_FROM', query_from), 
          ('QUERY_TO', query_to), 
          # ('RESULTS_FILE',...), - Can we use this parameter? 
          ('SEARCHSP_EFF', searchsp_eff), 
          ('SERVICE', service), 
          ('TEMPLATE_TYPE', template_type), 
          ('TEMPLATE_LENGTH', template_length), 
          ('THRESHOLD', threshold), 
          ('UNGAPPED_ALIGNMENT', ungapped_alignment), 
          ('WORD_SIZE', word_size), 
          ('CMD', 'Put'), 
          ] 
      query = [x for x in parameters if x[1] is not None] 
      message = _as_bytes(_urlencode(query)) 
   
      # Send off the initial query to qblast. 
      # Note the NCBI do not currently impose a rate limit here, other 
      # than the request not to make say 50 queries at once using multiple 
      # threads. 
      request = _Request(url_base, 
                         message, 
                         {"User-Agent": "BiopythonClient"}) 
      handle = _urlopen(request) 
   
      # Format the "Get" command, which gets the formatted results from qblast 
      # Parameters taken from http://www.ncbi.nlm.nih.gov/BLAST/Doc/node6.html on 9 July 2007 
      rid, rtoe = _parse_qblast_ref_page(handle) 
      parameters = [ 
          ('ALIGNMENTS', alignments), 
          ('ALIGNMENT_VIEW', alignment_view), 
          ('DESCRIPTIONS', descriptions), 
          ('ENTREZ_LINKS_NEW_WINDOW', entrez_links_new_window), 
          ('EXPECT_LOW', expect_low), 
          ('EXPECT_HIGH', expect_high), 
          ('FORMAT_ENTREZ_QUERY', format_entrez_query), 
          ('FORMAT_OBJECT', format_object), 
          ('FORMAT_TYPE', format_type), 
          ('NCBI_GI', ncbi_gi), 
          ('RID', rid), 
          ('RESULTS_FILE', results_file), 
          ('SERVICE', service), 
          ('SHOW_OVERVIEW', show_overview), 
          ('CMD', 'Get')] 
      query = [x for x in parameters if x[1] is not None] 
      message = _as_bytes(_urlencode(query)) 
   
      # Poll NCBI until the results are ready.  Use a backoff delay from 2 - 120 second wait 
      delay = 2.0 
      previous = time.time() 
      while True: 
          current = time.time() 
          wait = previous + delay - current 
          if wait > 0: 
              time.sleep(wait) 
              previous = current + wait 
          else: 
              previous = current 
          if delay + .5 * delay <= 120: 
              delay += .5 * delay 
          else: 
              delay = 120 
   
          request = _Request(url_base, 
                             message, 
                             {"User-Agent": "blastpy"}) 
          handle = _urlopen(request) 
          results = _as_string(handle.read()) 
   
          # Can see an "\n\n" page while results are in progress, 
          # if so just wait a bit longer... 
          if results == "\n\n": 
              continue 
          # XML results don't have the Status tag when finished 
          if "Status=" not in results: 
              break 
          i = results.index("Status=") 
          j = results.index("\n", i) 
          status = results[i + len("Status="):j].strip() 
          if status.upper() == "READY": 
              break 
   
      return StringIO(results) 

    def query_ncbi(self):
        """
            Perform query to NCBI and return results
        """