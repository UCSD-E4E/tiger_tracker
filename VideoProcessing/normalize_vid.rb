
# VideoNormalizer
# Class designed to correct the duration of videos taken with
# the camera trap since the OpenCV videoWriter is tricky
# to stabilize the frame rate
#
# Usage: In directory with videos to convert, run:
#        ruby normalize_vid.rb
#
# Author: Riley Yeakle

class VideoNormalizer  
  attr_accessor :video_names
  attr_accessor :video_durations
  
  def initialize(out_dir)
    @out_directory = out_dir  
    `mkdir ./#{out_dir}`
  end

  def getSeconds(duration_string)
    hours = duration_string[0,2].to_i 
    minutes = duration_string[3,2].to_i
    seconds = duration_string[6,2].to_i
    length_secs = (hours * 3600) + (minutes * 60) + seconds
  end

  def getNames(ext_string)
    raw_names = `ls | grep #{ext_string}`
   @video_names = raw_names.scan(/\S+/)
  end

  def getDurations
    length_array = []
    
    for i in (0...@video_names.length)
      cmd_str =  "ffmpeg -i ./#{@video_names[i]} 2>&1 | grep Duration: "
      output = `#{cmd_str}`
      p output
      raw_str = output [/Duration: [0-9:.]+/]
      duration_str = raw_str[/[0-9:.]+$/]
      length_array.push(getSeconds(duration_str))
      @video_durations = length_array
    end
  end

  def normalize_videos
    for i in (0...@video_names.length)
      pts_rate = 300.0/@video_durations[i] 
      cmd_str = "ffmpeg -i ./#{@video_names[i]} -r 25 -vf 'setpts=#{pts_rate}*PTS' -b 100k ./#{@out_directory}/#{@video_names[i]}" 
      `#{cmd_str}`
      puts "Percent done: %d" % ((i+1)*100/@video_names.length)
    end
  end  

end

vn = VideoNormalizer.new("out")

vn.getNames(".mp4")
vn.getDurations

p vn.video_names
p vn.video_durations

vn.normalize_videos

