require 'nokogiri'
require 'twitter'
require 'json'
require 'yaml'

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

