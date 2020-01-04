"""
TESTING CODE
"""

"""
tv_filename_key = tv_file[0].rsplit('/', 1)[-1]
tv_filetype_key = tv_file[0].rsplit('.', 1)[1]
tv_title_and_year_key = tv_file[0].rsplit('/')[-2]
tv_year_key = tv_file[0].rsplit('/')[-2].rsplit('(')[-1][:-1]


if tv_file[0] not in tv_results_list:
    if not tv_filename_key.lower().endswith('.nfo'):
        tv_results_list[tv_file[0]] = {}
        

tv_file_size = os.path.getsize(tv_file[0])
tv_file_size_in_mb = (int(tv_file_size) / 1048576)
tv_file_size_in_mb_rounded = str(round(tv_file_size_in_mb, 2))
tv_hash = str(str(tv_filename_key) + '_' + str(tv_file_size))


tv_results_list[tv_file[0]]['MEDIA-PATH'] = tv_file[0]
tv_results_list[tv_file[0]]['MEDIA-TYPE'] = str('TV SHOW')
tv_results_list[tv_file[0]]['FOLDER-NAME'] = tv_title_key
tv_results_list[tv_file[0]]['FILE-NAME'] = tv_filename_key
tv_results_list[tv_file[0]]['FILE-SIZE'] = tv_file_size_in_mb_rounded
tv_results_list[tv_file[0]]['TV-HASH'] = tv_hash
tv_results_list[tv_file[0]]['FILE-TYPE'] = tv_filetype_key


for found_tv_episodes in tv_results_list.items():
    print(found_tv_episodes)
    

IMDb().update(found_result, 'episodes')


if found_result not in tv_episodes_dict:
    tv_episodes_dict[found_result] = {}


for found_tv_plots in tv_overview_plots_dict.items():
    if str(found_tv_plots[1]['SHOW']).lower() == str(tv_title_key).lower():
        if str(found_tv_plots[1]['PLOT']).lower() == str('NO PLOT AVAILABLE').lower():
            tv_overview_plots_nfo_list.append(found_tv_plots)
            

for plot_review_items in tv_overview_plots_nfo_list:

    with open(os.path.expanduser((index_folder + '/TV_VIDEO_FILES_PATHS.csv').format(username)),
              encoding='UTF-8') as m_f_p_2:
        tv_index = csv.reader(m_f_p_2)

        for checked_tv_file in sorted(tv_index):
            if tv_filename_key.lower().endswith('.nfo'):
                if str(tv_title_key).lower() in str(plot_review_items[0]).lower():
                    if str(tv_filename_key).lower() == str('tvshow.nfo').lower():
                        with open(checked_tv_file[0]) as nfo_file:
                            for line in nfo_file.readlines():
                                if '<plot>' in line:
                                    formatted_plot = remove_html_tags(line)
                                    tv_overview_plots_dict[tv_title_key]['PLOT'] = formatted_plot.strip()
                                    

for items in tv_overview_plots_dict.items():
    print(items)
    
    
fname = pathlib.Path(tv_file[0])


with open(fname.parent / 'tvshow.nfo', 'r') as f:
    print(f.read())
    
                               
with open(os.path.expanduser((index_folder + '/TV_INFORMATION_INDEX.csv').format(username)), 'w',
          encoding='UTF-8', newline='') as m_i_i:

    csv_writer = csv.DictWriter(m_i_i, ['MEDIA-PATH', 'MEDIA-TYPE', 'FOLDER-NAME', 'FILE-NAME', 'FILE-SIZE',
                                        'FILE-TYPE', 'RESOLUTION', 'GUESSIT SEARCH TERM', 'TV SHOW ID #',
                                        'TV SHOW TITLE', 'SEASON #', 'EPISODE #', 'EPISODE TITLE', 'YEAR', 'PLOT',
                                        'RATING', 'RUN-TIME', 'GENRES', 'SEARCH CONFIDENCE PERCENTAGE', 'TV-HASH'])

    for tv_row in tv_results_list.values():
        csv_writer.writerow(tv_row)

with open(os.path.expanduser((index_folder + '/TV_PLOTS_INDEX.csv').format(username)), 'w',
          encoding='UTF-8', newline='') as t_p_i:
    csv_writer = csv.DictWriter(t_p_i, ['SHOW', 'PLOT'])
    for tv_row in tv_overview_plots_dict.values():
        csv_writer.writerow(tv_row)

tv_scan_end = time.time()
readable_tv_scan_time = round(tv_scan_end - tv_scan_start, 2)
print('TV INFORMATION SCAN COMPLETE - TIME ELAPSED: ', readable_tv_scan_time, 'Seconds')
separator_3()
"""
