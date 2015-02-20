wpscan
======

A Wordpress Malware Scanner
---------------------------
Articles on Wordpress Malware Analysis & Remediation  
http://blog.sucuri.net/2012/07/website-malware-removal-wordpress-tips-tricks.html  
http://wp.smashingmagazine.com/2012/10/09/four-malware-infections-wordpress/  
http://cantonbecker.com/work/musings/2009/how-to-search-for-backdoors-in-a-hacked-wordpress-site/  
http://blog.sucuri.net/2012/10/dealing-with-todays-wordpress-malware.html  
http://blog.sucuri.net/2012/08/sitecheck-got-blackhat-seo-spam-warning.html  
http://wordpress.org/tags/hacked  
http://wordpress.org/tags/malware  

Steps
----
Search for all evals - not necessarily malicious  
    grep -R eval * | more  
Grep for additional 'malicious' code  
    grep -RPl --include=*.{php} "(system|exec|passthru|shell_exec|fopen|fclose|filesman|edoced_46esad|gzuncompress|base64_decode|eval|) *\(" /path to file/  
Find any php files in the uploads directory  
    find uploads -name "*.php" -print  
Detect Recent Changes  
    find -type f -ctime -0 | more  
    find ./ -mtime -1  
Detect Changes outside of Normalized Timeframe  
    find . -mtime -10 -print  
Detect Differences (compare to a vanilla install)  
    diff -qr /path/dir1 /path/dir2  
Check theme index.php for things like:  
    $wp_theme_icon=@create_function(",@file_get_contents('/public_html/wp-content/themes/awesome_directory/s.jpg"));$wp_theme_icon();  
Check for PHP iFrame injections  
    is this right?  grep -Ri "<iframe width....................................>/iframe>"  
Check for Malicious Redirects  
    redirects user to a domain distributing malware  
    most likely in .htaccess file  
    find /var/www -name .htaccess -type f | wc -l  
        look for things like:  
        RewriteCond %{HTTP_REFERER} .*referringdomain.com.*$ [NC,OR]  
        RewriteRule .* http://baddomain.com [R,L]  

Notes
-----
catagorize search terms by level of maliciousness (group in lists)  
    generic search function that takes a list, path and recursion flag  
    i.e. search_files(terms, path, recursive=True)  
heuristic analysis - prioritize results based on the likliness of infection  
herusistic analysis - how to destinguish between likely malicious JS/PHP and nonmalicious  
search for file signiture/ext mismatches  
identify binary files, perform some sort of analysis, copy them out to reports directory for further analysis - integration with cuckoo possible?  
