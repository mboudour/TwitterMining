script_dir='/Users/mosesboudourides/GithubRepositories/TwitterMining/'

Dir.chdir script_dir
require_relative script_dir+'nokogiri_get_tweet_ids'
# out_dir='/home/sergios-len/Documents/githubs/TwitterMining/Output'
# auth_dir='/home/sergios-len/Documents/githubs/TwitterMining/credentials/auth_cred.txt'
# auth_dir='/home/mab/github_repos/TwitterMining/credentials/auth_cred.txt'
auth_dir='/Users/mosesboudourides/twitTemp/credentials/auth_cred.txt'
# Dir.chdir out_dir

out_dir='/Users/mosesboudourides/twitTemp/Output'

full_search_names,list_of_tweets,hash_of_tweets=parse_html(out_dir)
puts hash_of_tweets
folo=File.join(out_dir,"twetts_ids_#{full_search_names.uniq.join('_')}.ids")
puts " #{list_of_tweets.flatten.count} ids found"
File.open(folo, "w"){|to_file| list_of_tweets.each {|uu| to_file.write(uu.to_json+ "\n")}}
id_list = list_of_tweets.flatten.uniq.each_slice(100)
authkeys=auth_parse(auth_dir)

client= auth_client(authkeys)
json_list = Array.new()
id_list.each  do |u| 

    begin
    json_list <<  client.statuses(u)
    rescue Twitter::Error::TooManyRequests => error
        puts 'Waiting for 15...or better...'
        sleep error.rate_limit.reset_in + 1
        retry

    end
end

fololo=File.join(out_dir,"#{full_search_names.uniq.join('_')}_hash.json")

jj = json_list.flatten.uniq.collect {|u|  u.to_hash}
File.open(fololo,'a') {|to_file| jj.each {|uu| to_file.write(uu.to_json+ "\n")}}
puts "#{jj.count} tweets found!!!!"
p "Saved as #{fololo}"