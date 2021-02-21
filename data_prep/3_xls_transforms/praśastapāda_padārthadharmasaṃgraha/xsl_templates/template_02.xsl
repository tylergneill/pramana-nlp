<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" encoding="UTF-8">
<xsl:output method="xml" indent="yes"/>
<xsl:strip-space elements="*" />
 
<xsl:template match="TEI/text/body">

	<body>

        <xsl:for-each select="./div">	
			<div>
			<xsl:copy-of select="./head"/>

			<xsl:for-each select="./p">	
				<p>

				<xsl:copy-of select="./@*"/>

				<xsl:variable name="curr_n" select="@n"/>
				<xsl:attribute name="n2">
				<xsl:value-of select="count(preceding-sibling::p[@n=$curr_n])"/>
				</xsl:attribute>

				<xsl:attribute name="pb">
				<xsl:value-of select="./pb/@n"/>
				</xsl:attribute>

				<xsl:copy-of select="./node()[not(self::pb)]"/>

				</p>

			</xsl:for-each>

			</div>
        </xsl:for-each>

	</body>
	
</xsl:template>

<!-- 

<xsl:template match="div">

<xsl:for-each select="p[@n]">

{"<xsl:value-of select="@n"/>"}

[<xsl:number count="div"/>.<xsl:number count="p"/>]

<xsl:value-of select="."/>
</xsl:template>


<xsl:template match="head">

{<xsl:value-of select="."/>}

</xsl:template>
 -->


</xsl:stylesheet>