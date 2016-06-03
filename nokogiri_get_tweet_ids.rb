require 'nokogiri'
require 'twitter'
require 'json'
require 'yaml'

def auth_dici_n(key)
    auths_dict = File.open('auth_dic.yaml'){|ff| YAML.load( ff)}
    au = auths_dict.keys
    begin
        return auths_dict[key.next] , key.next if auths_dict.keys.include? key.next 
        return auths_dict[au[0]] , au[0]
    rescue Exception => e
        puts e
        puts "key #{key} not in #{au}"
        return auths_dict[1]
    end   
    end
def auth_client auth_new
    client = Twitter::REST::Client.new do |config|
      config.consumer_key        = auth_new["CONSUMER_KEY"]
      config.consumer_secret     = auth_new["CONSUMER_SECRET"]
      config.access_token        = auth_new["OAUTH_TOKEN"] 
      config.access_token_secret = auth_new["OAUTH_TOKEN_SECRET"]
    end
    return client
end
def auth_parse filename
    auth_keys=Hash.new
    File.open(filename,'r') do |file|
        file.readlines.each do |line|
            kv=line.split(' , ') 
            auth_keys[kv[0]] = kv[1].strip
        end
    end
    return auth_keys
end



def parse_html html_path
    html_npath=File.join(html_path,'**/*.out')
    filepaths = Dir.glob(html_npath)
    raise 'No .out files found!!!!' if filepaths.empty?

    full_search_names=Array.new
    list_of_tweets=Array.new
    hash_of_tweets = Hash.new 
    filepaths.each do |filepath|
        doc= File.open(filepath) { |f| Nokogiri::HTML(f)}

        doc_tid=doc.css('ol#stream-items-id.stream-items.js-navigable-stream').css('li').select{|u| u[:id]}
        filpah = filepath.split('/')[-1].split('_')[1]
        puts "Found #{doc_tid.count} tweets... for #{filpah}"
        hash_of_tweets.has_key?(filpah) ? hash_of_tweets[filpah] += doc_tid.count : hash_of_tweets[filpah] = doc_tid.count
        list_of_tweets_p = doc_tid.map{|f| f['data-item-id']}
        full_search_names << filpah 
        list_of_tweets << list_of_tweets_p
    end
    return full_search_names,list_of_tweets,hash_of_tweets
end

# puts hash_of_tweets

# puts full_search_names
# nfull_searc_names = full_search_names.select{|u| u+'_'}


# # client = Twitter::REST::Client.new do |config|
# #   config.consumer_key        = ""
# #   config.consumer_secret     = ""
# #   config.access_token        = ""
# #   config.access_token_secret = ""
# # end
# folo = "twetts_ids_#{full_search_names.uniq.join('_')}.ids_json"
# puts " #{list_of_tweets.flatten.count} ids found"
# File.open(folo, "w"){|to_file| list_of_tweets.each {|uu| to_file.write(uu.to_json+ "\n")}}
# id_list = list_of_tweets.flatten.uniq.each_slice(100)
# client=  
# # client ,key = auth_client 13
# json_list = Array.new()
# # json_list = 
# id_list.each  do |u| 

#     begin
#     json_list <<  client.statuses(u)
#     rescue Twitter::Error::TooManyRequests => error
#         puts 'Waiting for 15...or better...'
#         sleep error.rate_limit.reset_in + 1
#         retry

#     end
# end

# # folo = "twetts_#{full_search_names.uniq.join('_')}.json"
# # File.open(folo,'w') {|to_file| json.each {|uu| to_file.write(uu.to_json+ "\n")}}

# # File.open(folo, "w"){|to_file| Marshal.dump(json_list, to_file)}
# # puts folo

# # jj=json_list.flatten.uniq.collect {|u|  u.to_hash}
# puts "#{jj.count} tweets found!!!!"

# # If you want to work in ruby yaml is great
# # fololo = "#{full_search_names.uniq.join('_')}_hash.yaml"
# # File.open(fololo, "w"){|to_file| YAML.dump(jj, to_file)}
# # 
# fololo = "#{full_search_names.uniq.join('_')}_hash.json"

# jj = json_list.flatten.uniq.collect {|u|  u.to_hash}
#       File.open(fololo,'a') {|to_file| jj.each {|uu| to_file.write(uu.to_json+ "\n")}}

