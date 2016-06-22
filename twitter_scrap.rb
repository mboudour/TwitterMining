require 'capybara'
require 'yaml'
require 'timeout'
require 'fileutils'
require 'date'
require 'nokogiri'
require 'pry'

def try_a_few_times(how_many=10, tries=0, &block)
    begin
      yield
    rescue Exception => exception
      raise exception if tries > how_many
      p exception,tries #if Environment.debug?
      sleep 1
      try_a_few_times how_many, tries + 1, &block
    end
  end
def with_time_zone(tz_name)
  prev_tz = ENV['TZ']
  ENV['TZ'] = tz_name
  yield
ensure
  ENV['TZ'] = prev_tz
end
class  SearchTwitter
    def initialize(searchterm, from, to, last = 600,hashtag=true)
        Capybara.register_driver :selenium do |app|
          Capybara::Selenium::Driver.new(app, :browser => :chrome)
        end
        @searchterm = searchterm
        @from = from
        @to = to
        @browser = Capybara::Session.new(:selenium)
        if hashtag
            remote_base_url = "https://twitter.com/search?q=%23#{@searchterm}%20since%3A#{@from}%20until%3A#{@to}&src=typd"
        else
            remote_base_url = "https://twitter.com/search?q=#{@searchterm}%20since%3A#{@from}%20until%3A#{@to}&src=typd"
        end
        @browser.visit remote_base_url
    end

    def scrap_twitter_page pages,ccc, overpa = 0
        cccc = ccc
        (1..pages).each do |page|
            puts "Downloading page: " + (overpa + page).to_s
            begin
                @browser.execute_script 'window.scrollBy(0,2000)'
                if page == cccc 
                    puts 'show to show stats, q to quit!'
                    # @browser.save_screenshot("scr_#{page}.png")
                    ready_fds = select [ $stdin ], [], [], 10
                    ready_fds_val = ready_fds.first.first.gets unless ready_fds.nil?
                    break if  ready_fds_val == "q\n"
                    if ready_fds_val == "show\n"
                        begin
                            pager = @browser.find('ol#stream-items-id.stream-items.js-navigable-stream')
          
                            # if counter_t < pager.all('li').count then counter_t = pager.all('li').count end
                            p  pager.all('li').count
                        rescue Exception => e
                            p e
                        end
                        # break
                    end
                    cccc+=ccc
                end
            rescue Exception => e
                p e
              open("test_myfile_#{page}.out", 'w') { |f|
              f.puts @browser.html
            }
              @browser.save_screenshot("scr_#{page}.png")#, :full => true)
            puts 'q for exit '
              ser=gets()

              sleep ser unless ser=='q'
              Capybara.current_session.driver.quit if ser=='q' 
              
              break if ser=='q'
            end
              sleep 1

        end
    end
    def get_date
        begin
            sleep 25
            html = try_a_few_times { Nokogiri::HTML(@browser.html.to_s)}
            doc_tid=html.css('ol#stream-items-id.stream-items.js-navigable-stream').css('li').select{|u| u[:id]}.count
            ddoc= html.at_xpath("/html/body/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/ol[1]/li[#{doc_tid}]/div/div[2]/div[1]/small/a")
            if ddoc.nil?
            ddoc = html.at_xpath("/html/body/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[2]/ol[1]/li[#{doc_tid}]/ol/li/div/div[2]/div[1]/small/a")
            end
            going_up =1
            while ddoc.nil?  do
                ddoc= html.at_xpath("/html/body/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/ol[1]/li[#{doc_tid-going_up}]/div/div[2]/div[1]/small/a")
                if ddoc.nil?
                ddoc = html.at_xpath("/html/body/div[2]/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div/div/div[2]/ol[1]/li[#{doc_tid-going_up}]/ol/li/div/div[2]/div[1]/small/a")
                end
                going_up += 1
                break if doc_tid < going_up
            end
            
            puts "Found #{doc_tid} ids until #{ddoc[:title]}"
            return   DateTime.parse(ddoc[:title])
        rescue Exception => e
            p e
            puts e
            # binding.pry
            begin
                sleep 80
                html = Nokogiri::HTML(@browser.html.to_s)
                doc_tid=html.css('ol#stream-items-id.stream-items.js-navigable-stream').css('li').select{|u| u[:id]}.count
                ddoc= html.at_xpath("/html/body/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/ol[1]/li[#{doc_tid}]/div/div[2]/div[1]/small/a")
                going_up =1
                while ddoc.nil?  do
                    ddoc= html.at_xpath("/html/body/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/ol[1]/li[#{doc_tid-going_up}]/div/div[2]/div[1]/small/a")
                    going_up += 1
                    break if doc_tid < going_up
                    
                end
                puts "Found #{doc_tid} ids until #{ddoc[:title]}"
                return   DateTime.parse(ddoc[:title])
            rescue Exception => e
                # binding.pry
                puts e
            end
        end
    end
    # def get_date
    #     begin
    #         sleep 25
    #         html = Nokogiri::HTML(@browser.html.to_s)
    #         doc_tid=html.css('ol#stream-items-id.stream-items.js-navigable-stream').css('li').select{|u| u[:id]}.count
    #         ddoc= html.at_xpath("/html/body/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/ol[1]/li[#{doc_tid}]/div/div[2]/div[1]/small/a")
    #         puts "Found #{doc_tid} ids until #{ddoc[:title]}"
    #         return   DateTime.parse(ddoc[:title])
    #     rescue Exception => e
    #         p e
    #         puts e
    #         begin
    #             sleep 80
    #             html = Nokogiri::HTML(@browser.html.to_s)
    #             doc_tid=html.css('ol#stream-items-id.stream-items.js-navigable-stream').css('li').select{|u| u[:id]}.count
    #             ddoc= html.at_xpath("/html/body/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/ol[1]/li[#{doc_tid}]/div/div[2]/div[1]/small/a")
    #             puts "Found #{doc_tid} ids until #{ddoc[:title]}"
    #             return   DateTime.parse(ddoc[:title])
    #         rescue Exception => e
    #             puts e
    #         end
    #         # p e

    #     end
    # end
    def write_html
        dirnn = "#{@searchterm}__#{@from}/"
        puts dirnn
        puts Dir.pwd
        Dir.mkdir dirnn unless File.exists? dirnn

        ddirnam=dirnn + "myfile_#{@searchterm}_#{@from}_#{@to}.out"
        open(ddirnam, 'w') { |f|  f.puts @browser.html}
    end
    def close_search
        @browser.driver.quit
    end
    
end
# searchterm='parisattacks' 
# # searchterm='day%20night%20paris' #hashtag=false
# from='2015-12-20'
# pages = 500
# cccc = 50
# to = '2016-02-26'
# check = nil

# begin

#     gaza_searc = SearchTwitter.new(searchterm,from,to,hashtag=true)
#     gaza_searc.scrap_twitter_page(pages,cccc)
#     new_to = gaza_searc.get_date
#     p check,new_to, 'check first'
#     if check == new_to
#         gaza_searc.write_html
#         gaza_searc.close_search
#         puts 'Finaly'
#         break
#     end

        
#     new_to_day = new_to.prev_day.day
#     puts new_to.hour
#     if  Date.new(new_to.year,new_to.mon,new_to.mday).to_s <= from
#         gaza_searc.write_html
#         gaza_searc.close_search
#         puts 'GoGo'
#         break
    
#     elsif new_to.hour < 8 
#         npages = pages
#         begin
#             gaza_searc.scrap_twitter_page(cccc * 2 , 25,npages)
#             new_to = gaza_searc.get_date
#             if check == nil 
#                 check= new_to
#             elsif check > new_to
#                 check = new_to
#             elsif check == new_to
#                 puts 'I m out'
#                 break   
#             end
#             npages += cccc*2
#         end until (new_to.day <=> new_to_day) == -1 
#     end
#     puts 'Still in loop'
#     nto= new_to.next
#     to = Date.new(nto.year,nto.mon,nto.mday).to_s
#     tot = Date.new(new_to.year,new_to.mon,new_to.mday).to_s
#     puts to,tot
#     gaza_searc.write_html
#     gaza_searc.close_search
# end until from == tot 
