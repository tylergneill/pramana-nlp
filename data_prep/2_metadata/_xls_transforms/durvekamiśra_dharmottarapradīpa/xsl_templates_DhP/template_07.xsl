<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />

<xsl:template match="@*|node()">
<xsl:copy>
<xsl:apply-templates select="@*|node()"/>
</xsl:copy>
</xsl:template>

<xsl:template match="TEI/text/body">

	<body>
	<xsl:copy-of select="./text()"/>

        <xsl:for-each select="./div">	
			<div>

			<xsl:for-each select="./p">	
				<p>

				<xsl:copy-of select="./@*"/>

				<xsl:variable name="curr_pb" select="@pb"/>
				<xsl:variable name="curr_ll" select="@ll"/>
				<xsl:attribute name="p_n">
				<xsl:value-of select="count(preceding::p[@pb=$curr_pb and @ll=$curr_ll])+1"/>
				</xsl:attribute>
				<xsl:attribute name="ll_n">
				<xsl:value-of select="count(preceding::p[@ll=$curr_ll])+1"/>
				</xsl:attribute>

				<xsl:copy-of select="./node()"/>

				</p>

			</xsl:for-each>

			</div>
        </xsl:for-each>

	</body>
	
</xsl:template>

</xsl:stylesheet>